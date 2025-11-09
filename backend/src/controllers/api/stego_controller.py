import os
from fastapi import (
    APIRouter, UploadFile, File, Form, Depends, status, HTTPException, Request
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional, List

from src.schemas.sign_schema import SignatureResponse, SignatureListItem
from src.schemas.sign_verif_schema import SignatureVerificationResponse, VerificationListItem
from src.schemas.base_schema import BaseErrorResponse
from src.services.stego_service import StegoService
from src.dependencies.injection import get_db, get_current_user, get_stego_service
from src.models import User
import base64

router = APIRouter(
    prefix="/stego",
    tags=["Steganography"],
    responses={
        401: {"model": BaseErrorResponse, "description": "Unauthorized"},
        500: {"model": BaseErrorResponse, "description": "Internal Server Error"},
    },
)


@router.post(
    "/upload-signature",
    response_model=SignatureResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Image signée et stockée avec succès."},
        400: {"model": BaseErrorResponse, "description": "Entrée invalide"},
    },
)
def upload_signature_image(
    message: str = Form(...),
    file: UploadFile = File(...),
    encryption: str = Form("aes"),
    encryption_key: Optional[str] = Form(None),
    request: Request = None,
    current_user: User = Depends(get_current_user),
    stego_service: StegoService = Depends(get_stego_service),
):
    #  Vérification du type de fichier
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier doit être une image.")

    #  Appel du service métier
    response = stego_service.create_signature(
        user_id=current_user.id,
        image_file=file,
        message=message,
        encryption=encryption,
        encryption_key=encryption_key,
    )

    # Génération du lien de téléchargement
    response.download_url = str(
        request.url_for("download_signed_image", signature_uuid=response.signature_uuid)
    )

    return response


@router.post(
    "/verify",
    response_model=SignatureVerificationResponse,
    status_code=status.HTTP_200_OK,
)
def verify_image_signature(
    file: UploadFile = File(...),
    encryption_key: Optional[str] = Form(None),
    rsa_private_pem: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    stego_service: StegoService = Depends(get_stego_service),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier doit être une image.")

    return stego_service.verify_signature(
        user_id=current_user.id,
        file=file,
        encryption_key=encryption_key,
        rsa_private_pem=rsa_private_pem
    )


@router.get(
    "/signatures",
    response_model=List[SignatureListItem],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "List of user signatures."},
        401: {"model": BaseErrorResponse, "description": "Unauthorized"},
    },
)
def get_user_signatures(
    current_user: User = Depends(get_current_user),
    stego_service: StegoService = Depends(get_stego_service),
):
    """Récupère toutes les signatures créées par l'utilisateur actuel."""
    return stego_service.get_user_signatures(current_user.id)


@router.get(
    "/verifications",
    response_model=List[VerificationListItem],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "List of user verifications."},
        401: {"model": BaseErrorResponse, "description": "Unauthorized"},
    },
)
def get_user_verifications(
    current_user: User = Depends(get_current_user),
    stego_service: StegoService = Depends(get_stego_service),
):
    """Récupère toutes les vérifications effectuées par l'utilisateur actuel."""
    return stego_service.get_user_verifications(current_user.id)

@router.get(
    "/download/{signature_uuid}",
    responses={
        200: {"content": {"image/png": {}}},
        404: {"model": BaseErrorResponse, "description": "Signature non trouvée"},
    },
)
def download_signed_image(
    signature_uuid: str,
    current_user: User = Depends(get_current_user),
    stego_service: StegoService = Depends(get_stego_service),
):
    """
    Télécharge l'image signée associée à un UUID.
    """
    signed_path = stego_service.get_signed_image_path(signature_uuid)
    if not signed_path or not os.path.exists(signed_path):
        raise HTTPException(status_code=404, detail="Image signée introuvable.")

    # Read the image file and encode to base64
    
    with open(signed_path, "rb") as image_file:
        image_data = image_file.read()
        base64_encoded = base64.b64encode(image_data).decode('utf-8')
    
    return {
        "filename": os.path.basename(signed_path),
        "media_type": f"image/{signed_path.split('.')[-1]}",
        "base64_data": base64_encoded
    }
