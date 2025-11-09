from sqlalchemy import inspect
from sqlalchemy.orm import Session
from src.models.role import Role

DEFAULT_ROLES = [
    {"name": "admin", "description": "Administrateur"},
    {"name": "end_user", "description": "Utilisateur final"},
]

def seed_roles(db: Session):
    inspector = inspect(db.bind)
    if not Role.__tablename__ in inspector.get_table_names():
        return
    for role in DEFAULT_ROLES:
        if not db.query(Role).filter_by(name=role["name"]).first():
            db.add(Role(**role))
    db.commit()
