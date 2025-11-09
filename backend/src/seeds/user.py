from sqlalchemy import inspect
from sqlalchemy.orm import Session

from src.models.user_role import UserRole
from src.models.user_status import UserStatus
from src.core.config import settings
from src.utils.security import get_password_hash
from src.models.role import Role
from src.models.status import Status
from src.models.user import User
from src.schemas.role_schema import RoleEnum
from src.schemas.status_schema import StatusEnum
from src.models.password_history import PasswordHistory

DEFAULT_USERS = [
    {
        "firstname": "Admin",
        "lastname": "User",
        "username": "admin",
        "email": settings.DEFAULT_ADMIN_EMAIL,
        "password": settings.DEFAULT_ADMIN_PASSWORD,
        "roles": [RoleEnum.ADMIN],
        "status_history": [StatusEnum.ACTIVE]
    }
]

def seed_users(db: Session):
    inspector = inspect(db.bind)
    if not User.__tablename__ in inspector.get_table_names():
        return
    for user_data in DEFAULT_USERS:
        if not db.query(User).filter_by(email=user_data["email"]).first():
            user = User(
                firstname=user_data["firstname"],
                lastname=user_data["lastname"],
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
            )

            db.add(user)
            db.flush()

            password_history = PasswordHistory(
                user_id=user.id,
                password=user.hashed_password
            )
            db.add(password_history)

            for role in user_data["roles"]:
                role = db.query(Role).filter_by(name=role).first()
                if role:
                    user_role = UserRole(
                        user_id=user.id,
                        role_id=role.id
                    )
                    db.add(user_role)
            
            for status in user_data["status_history"]:
                status = db.query(Status).filter_by(name=status).first()
                if status:
                    user_status = UserStatus(
                        user_id=user.id,
                        status_id=status.id,
                        reason="Initial registration"
                    )
                    db.add(user_status)
    db.commit()

