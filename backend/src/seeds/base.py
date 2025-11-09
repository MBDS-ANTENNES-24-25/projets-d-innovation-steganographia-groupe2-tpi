from sqlalchemy.orm import Session

from .user import seed_users
from .role import seed_roles
from .status import seed_statuses

def seed_all(db: Session):
    seed_roles(db)
    seed_statuses(db)
    seed_users(db)
