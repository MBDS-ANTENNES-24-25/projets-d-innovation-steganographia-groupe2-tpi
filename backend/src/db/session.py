from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import get_database_url


db_url = get_database_url()
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
