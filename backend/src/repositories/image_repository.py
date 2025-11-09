import os
import uuid
from hashlib import sha256
from typing import Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session
from src.models import Image

MEDIA_DIR = os.path.abspath("src/media/images/")


class ImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_or_get(self, file: UploadFile, user_id: int) -> Image:
        """Enregistre l'image si elle n'existe pas déjà (via son hash)."""
        content = file.file.read()
        file.file.seek(0)
        file_hash = sha256(content).hexdigest()

        # Vérifier si déjà en base
        existing = self.db.query(Image).filter_by(sha256_hash=file_hash).first()
        if existing:
            return existing

        # Sauvegarder
        os.makedirs(MEDIA_DIR, exist_ok=True)
        # Extraire l'extension du fichier original
        file_extension = os.path.splitext(file.filename)[1] if file.filename else '.png'
        filename = f"{uuid.uuid4()}{file_extension}"
        path = os.path.join(MEDIA_DIR, filename)

        with open(path, "wb") as f:
            f.write(content)

        image = Image(
            user_id=user_id,
            file_path=path,
            original_filename=file.filename,
            mime_type=file.content_type,
            sha256_hash=file_hash,
        )
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    def save_temp(self, file: UploadFile) -> str:
        """Sauvegarde temporaire (ex: pour vérification)."""
        content = file.file.read()
        os.makedirs(MEDIA_DIR, exist_ok=True)
        temp_name = f"temp_{uuid.uuid4()}.png"
        path = os.path.join(MEDIA_DIR, temp_name)

        with open(path, "wb") as f:
            f.write(content)
        return path

    def get_by_id(self, image_id: int) -> Optional[Image]:
        """Récupère une image par son ID."""
        return self.db.query(Image).filter_by(id=image_id).first()
