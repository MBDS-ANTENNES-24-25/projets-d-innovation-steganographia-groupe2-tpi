from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base

class Signature(Base):
    __tablename__ = "signatures"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    signer_id = Column(Integer, nullable=False)
    signature_uuid = Column(String, unique=True, nullable=False)
    signed_at = Column(DateTime(timezone=True), server_default=func.now())

    image = relationship("Image", back_populates="signatures")
    verifications = relationship("Verification", back_populates="signature")