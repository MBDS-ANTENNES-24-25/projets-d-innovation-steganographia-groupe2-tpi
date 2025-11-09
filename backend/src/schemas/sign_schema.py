from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SignatureResponse(BaseModel):
    signature_uuid: str
    image_id: int
    file_path: str
    download_url: Optional[str] = None
    class Config:
        orm_mode = True


class SignatureListItem(BaseModel):
    id: int
    signature_uuid: str
    image_id: int
    signer_id: int
    signed_at: datetime
    original_filename: Optional[str] = None
    file_path: Optional[str] = None
    download_url: Optional[str] = None
    
    class Config:
        orm_mode = True