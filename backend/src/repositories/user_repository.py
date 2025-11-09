from typing import Optional
from sqlalchemy.orm import Session
from src.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int)-> Optional[User]:
        return self.db.query(User).filter_by(id=id).first()


    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter_by(username=username).first()


    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter_by(email=email).first()


    def create(self,firstname: str, lastname: str, username: str, email: str, hashed_password: str, commit: bool = True) -> User:
        user = User(
            firstname=firstname, 
            lastname=lastname, 
            username=username, 
            email=email, 
            hashed_password=hashed_password
        )
        self.db.add(user)
        self.db.flush()
        if commit:
            self.db.commit()
            self.db.refresh(user)
        return user
    
    
    def create_user_oauth(self, email: str, firstname: str, lastname: str, username: str, provider: str, commit: bool = True) -> User:
        user = User(
            email=email,
            firstname=firstname,
            lastname=lastname,
            username=username,
            is_oauth=True,
            oauth_provider=provider
        )
        self.db.add(user)
        self.db.flush()
        if commit:
            self.db.commit()
            self.db.refresh(user)
        return user

