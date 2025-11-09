from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SignatureVerificationResponse(BaseModel):
    valid: bool
    signature_uuid: Optional[str] = None
    author_id: Optional[int] = None
    message: Optional[str] = None
    signed_at: Optional[datetime] = None


class VerificationListItem(BaseModel):
    id: int
    signature_uuid: Optional[str] = None
    image_id: Optional[int] = None
    verifier_id: int
    verified: bool
    timestamp: datetime
    extracted_payload: Optional[str] = None
    
    class Config:
        orm_mode = True
