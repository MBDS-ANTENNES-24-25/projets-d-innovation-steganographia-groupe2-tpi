from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from src.db.base import Base

class Verification(Base):
    __tablename__ = "verifications"

    id = Column(Integer, primary_key=True, index=True)
    signature_uuid = Column(String, ForeignKey("signatures.signature_uuid"), nullable=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=True)
    verifier_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    verified = Column(Boolean, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    extracted_payload = Column(String, nullable=True)

    image = relationship("Image", back_populates="verifications")
    signature = relationship("Signature", back_populates="verifications")
    verifier = relationship("User", back_populates="verifications")