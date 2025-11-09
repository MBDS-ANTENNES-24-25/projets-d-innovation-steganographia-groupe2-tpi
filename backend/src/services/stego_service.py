import os
import json
from io import BytesIO
from typing import Optional

from cryptography.fernet import Fernet
from fastapi import UploadFile
from sqlalchemy.orm import Session

from src.repositories.image_repository import ImageRepository
from src.repositories.signature_repository import SignatureRepository
from src.repositories.verification_repository import VerificationRepository
from src.schemas.sign_schema import SignatureResponse, SignatureListItem
from src.schemas.sign_verif_schema import SignatureVerificationResponse, VerificationListItem
from src.models import Signature
from typing import List

from src.utils.stego_utils import embed_data_into_image, extract_data_from_image
from src.services.stegano_dct_service import SteganoDCTService
import importlib.util

# Import du module avec tiret dans le nom
_stegano_lsb_path = os.path.join(os.path.dirname(__file__), "stegano-lsb.py")
spec = importlib.util.spec_from_file_location("stegano_lsb", _stegano_lsb_path)
stegano_lsb_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stegano_lsb_module)
SteganoLSBService = stegano_lsb_module.SteganoLSBService

# clé par défaut (pour compatibilité / tests) — tu peux la remplacer / gérer par utilisateur
DEFAULT_FERNET_KEY = b"V4U3vLAVddPqktGCNF0hDgO3qIdJFa7mcqRg3b7EPMA="
MEDIA_DIR = os.path.abspath("media/")  # Dossier où stocker les images signées

class StegoService:
    def __init__(self, db: Session):
        self.db = db
        self.image_repo = ImageRepository(db)
        self.signature_repo = SignatureRepository(db)
        self.verification_repo = VerificationRepository(db)
        self.stegano_lsb = SteganoLSBService(db)
        self.stegano_dct = SteganoDCTService(db)
        os.makedirs(MEDIA_DIR, exist_ok=True)

    def create_signature(
        self,
        user_id: int,
        image_file: UploadFile,
        message: str,
        encryption: str = "aes",
        encryption_key: Optional[str] = None,
        password: Optional[str] = None,
        key_positions_secret: Optional[str] = None,
    ) -> SignatureResponse:
        image_record = self.image_repo.save_or_get(image_file, user_id)

        import uuid
        signature_uuid = str(uuid.uuid4())
        
        # Détecter le type d'image pour choisir la méthode de stéganographie
        file_extension = os.path.splitext(image_file.filename.lower())[1] if image_file.filename else ""
        original_extension = os.path.splitext(image_record.file_path.lower())[1]
        
        # Utiliser l'extension du fichier original si disponible
        extension = original_extension or file_extension
        
        signed_filename = f"signed_{signature_uuid}{extension}"
        signed_path = os.path.join(MEDIA_DIR, signed_filename)
        
        if extension in ['.bmp', '.bitmap']:
            # Utiliser LSB pour les bitmaps
            self.stegano_lsb.hide_message(
                input_path=image_record.file_path,
                output_path=signed_path,
                message=message,
                repeat=10
            )
        
        elif extension in ['.png', '.jpg', '.jpeg']:
            # Utiliser des valeurs par défaut si les paramètres DCT ne sont pas fournis
            if not password:
                password = f"_{user_id}_"
            if not key_positions_secret:
                key_positions_secret = f"_{user_id}_"
            
            # Utiliser DCT pour PNG et JPEG
            self.stegano_dct.embed_message_aes(
                in_path=image_record.file_path,
                out_path=signed_path,
                message=message,
                password=password,
                key_positions_secret=key_positions_secret,
                strength=24.0,
                redundancy=30,
                channel_choice="Y",
                jpeg_quality=100
            )
        
        else:
            # Par défaut, utiliser LSB pour les autres formats
            
            self.stegano_lsb.hide_message(
                input_path=image_record.file_path,
                output_path=signed_path,
                message=message,
                repeat=10
            )

        signature = self.signature_repo.create(
            image_id=image_record.id,
            signer_id=user_id,
            signature_uuid=signature_uuid,
        )

        return SignatureResponse(
            signature_uuid=signature.signature_uuid,
            image_id=image_record.id,
            file_path=signed_path,
        )

    def verify_signature(
        self,
        user_id: int,
        file: UploadFile,
        encryption_key: Optional[str] = None,
        rsa_private_pem: Optional[str] = None,
        password: Optional[str] = None,
        key_positions_secret: Optional[str] = None,
    ) -> SignatureVerificationResponse:
        # Sauvegarder temporairement le fichier pour extract_message
        temp_path = self.image_repo.save_temp(file)
        
        try:
            # Détecter le type d'image pour choisir la méthode de stéganographie
            file_extension = os.path.splitext(file.filename.lower())[1] if file.filename else ""
            temp_extension = os.path.splitext(temp_path.lower())[1]
            
            # Utiliser l'extension du fichier temporaire si disponible
            extension = temp_extension or file_extension
            
            if extension in ['.bmp', '.bitmap']:
                # Utiliser LSB pour les bitmaps
                extracted_message = self.stegano_lsb.extract_message(
                    image_path=temp_path,
                    repeat=5
                )
                
                # Si le message commence par "❌", c'est une erreur
                if extracted_message.startswith("❌"):
                    self.verification_repo.create(
                        signature_uuid=None,
                        verifier_id=user_id,
                        verified=False,
                        extracted_payload=extracted_message
                    )
                    return SignatureVerificationResponse(valid=False, message=extracted_message)
            
            elif extension in ['.png', '.jpg', '.jpeg']:
                # Utiliser des valeurs par défaut si les paramètres DCT ne sont pas fournis
                if not password:
                    password = f"_{user_id}_"
                if not key_positions_secret:
                    key_positions_secret = f"_{user_id}_"
                
                extracted_message = self.stegano_dct.extract_message_aes(
                    in_path=temp_path,
                    password=password,
                    key_positions_secret=key_positions_secret,
                    redundancy=30,
                    channel_choice="Y"
                )
            
            else:
                # Par défaut, essayer LSB pour les autres formats
                extracted_message = self.stegano_lsb.extract_message(
                    image_path=temp_path,
                    repeat=5
                )
                
                # Si le message commence par "❌", c'est une erreur
                if extracted_message.startswith("❌"):
                    self.verification_repo.create(
                        signature_uuid=None,
                        verifier_id=user_id,
                        verified=False,
                        extracted_payload=extracted_message
                    )
                    return SignatureVerificationResponse(valid=False, message=extracted_message)
            
            # Enregistrer la vérification réussie avec le message extrait
            self.verification_repo.create(
                signature_uuid=None,
                verifier_id=user_id,
                verified=True,
                extracted_payload=extracted_message
            )
            
            return SignatureVerificationResponse(
                valid=True,
                message=extracted_message
            )
            
        except Exception as e:
            error_message = f"Échec d'extraction: {str(e)}"
            self.verification_repo.create(
                signature_uuid=None,
                verifier_id=user_id,
                verified=False,
                extracted_payload=error_message,
            )
            return SignatureVerificationResponse(valid=False, message=error_message)
        finally:
            # Nettoyer le fichier temporaire
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except:
                pass

    def get_user_signatures(self, user_id: int) -> List[SignatureListItem]:
        """Récupère toutes les signatures créées par un utilisateur."""
        signatures = self.signature_repo.list_by_signer(user_id)
        result = []
        for sig in signatures:
            # Récupérer les informations de l'image associée
            image = self.image_repo.get_by_id(sig.image_id) if sig.image_id else None
            result.append(SignatureListItem(
                id=sig.id,
                signature_uuid=sig.signature_uuid,
                image_id=sig.image_id,
                signer_id=sig.signer_id,
                signed_at=sig.signed_at,
                original_filename=image.original_filename if image else None,
                file_path=image.file_path if image else None
            ))
        return result

    def get_user_verifications(self, user_id: int) -> List[VerificationListItem]:
        """Récupère toutes les vérifications effectuées par un utilisateur."""
        verifications = self.verification_repo.list_by_verifier(user_id)
        return [VerificationListItem(
            id=verif.id,
            signature_uuid=verif.signature_uuid,
            image_id=verif.image_id,
            verifier_id=verif.verifier_id,
            verified=verif.verified,
            timestamp=verif.timestamp,
            extracted_payload=verif.extracted_payload
        ) for verif in verifications]
        
    def get_signed_image_path(self, signature_uuid: str) -> Optional[str]:
        signature = self.signature_repo.get_by_uuid(signature_uuid)
        if not signature:
            return None

        # List of possible extensions to check
        extensions = ['.bmp', '.bitmap', '.png', '.jpg', '.jpeg']
        
        for ext in extensions:
            signed_filename = f"signed_{signature_uuid}{ext}"
            signed_path = os.path.join(MEDIA_DIR, signed_filename)
            if os.path.exists(signed_path):
                return signed_path
                
        return None

