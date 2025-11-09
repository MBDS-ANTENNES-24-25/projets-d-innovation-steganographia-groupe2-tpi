from sqlalchemy.orm import Session
from src.models import Signature


class SignatureRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, image_id: int, signer_id: int, signature_uuid: str) -> Signature:
        """Crée une nouvelle signature en base."""
        signature = Signature(
            image_id=image_id,
            signer_id=signer_id,
            signature_uuid=signature_uuid,
        )
        self.db.add(signature)
        self.db.commit()
        self.db.refresh(signature)
        return signature

    def get_by_uuid(self, signature_uuid: str) -> Signature:
        """Récupère une signature par son UUID."""
        return self.db.query(Signature).filter_by(signature_uuid=signature_uuid).first()

    def list_by_signer(self, signer_id: int) -> list[Signature]:
        """Récupère toutes les signatures créées par un utilisateur."""
        return (
            self.db.query(Signature)
            .filter(Signature.signer_id == signer_id)
            .order_by(Signature.signed_at.desc())
            .all()
        )
