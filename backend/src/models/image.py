from sqlalchemy import Column,Integer,String, DateTime, func
from sqlalchemy.orm import relationship
from src.db.base import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
    original_filename = Column(String)
    mime_type = Column(String)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    sha256_hash = Column(String, unique=True)

    signatures = relationship("Signature", back_populates="image")
    verifications = relationship("Verification", back_populates="image")
