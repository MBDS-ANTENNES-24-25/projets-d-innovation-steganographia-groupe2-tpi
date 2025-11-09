from sqlalchemy import inspect
from sqlalchemy.orm import Session
from src.models.status import Status

DEFAULT_STATUSES = [
    {
        "name": "active",
        "description": "Compte actif. L'utilisateur a confirmé son adresse e-mail ou s'est inscrit/connecté via OAuth et peut se connecter ou le compte a été réactivé après une suspension."
    },
    {
        "name": "inactive",
        "description": "Compte inactif. L'utilisateur n'a pas encore confirmé son adresse e-mail ou n'a pas activé son compte."
    },
    {
        "name": "suspended",
        "description": "Compte suspendu. L'utilisateur ne peut pas se connecter, généralement en raison d'une violation des conditions d'utilisation ou d'une action administrative."
    }
]

def seed_statuses(db: Session):
    inspector = inspect(db.bind)
    if not Status.__tablename__ in inspector.get_table_names():
        return
    for status in DEFAULT_STATUSES:
        if not db.query(Status).filter_by(name=status["name"]).first():
            db.add(Status(**status))
    db.commit()
