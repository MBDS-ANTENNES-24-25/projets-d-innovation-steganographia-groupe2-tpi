from typing import Optional
from sqlalchemy.orm import Session
from src.models import Verification


class VerificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        signature_uuid: Optional[str],
        verifier_id: int,
        verified: bool,
        image_id: Optional[int] = None,
        extracted_payload: Optional[str] = None,
    ) -> Verification:
        verification = Verification(
            signature_uuid=signature_uuid,
            image_id=image_id,
            verifier_id=verifier_id,
            verified=verified,
            extracted_payload=extracted_payload,
        )

        self.db.add(verification)
        self.db.commit()
        self.db.refresh(verification)
        return verification

    def get_by_id(self, verification_id: int) -> Optional[Verification]:
        return self.db.query(Verification).filter_by(id=verification_id).first()

    def list_by_signature(self, signature_uuid: str) -> list[Verification]:
        return (
            self.db.query(Verification)
            .filter(Verification.signature_uuid == signature_uuid)
            .order_by(Verification.timestamp.desc())
            .all()
        )

    def list_by_verifier(self, verifier_id: int) -> list[Verification]:
        return (
            self.db.query(Verification)
            .filter(Verification.verifier_id == verifier_id)
            .order_by(Verification.timestamp.desc())
            .all()
        )
