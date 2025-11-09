from contextlib import asynccontextmanager
import subprocess
from fastapi import FastAPI
from src.core.middleware import add_cors_middleware
from src.controllers.routes import include_routers
from src.exceptions.http_exception_handler import add_exception_handlers
from src.seeds.base import seed_all
from src.db.session import SessionLocal
from src.core.config import settings
from .logging import configure_logging, LogLevels
from src.controllers.api import stego_controller


configure_logging(LogLevels.debug if settings.DEBUG else LogLevels.info)

# Run database migrations if in development environment
if settings.ENV == "dev":
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
    except subprocess.CalledProcessError as e:
        pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed_all(db)
        yield
    finally:
        db.close()

app = FastAPI(
    title="Steganographia API", 
    version="1.0.0", 
    description="""
        API for Steganographia, a secure platform that embeds unique, compression-resistant image signatures during upload. 
        Authenticated users can sign images and later verify authorship via a dedicated feature. 
        The system ensures strong authentication, data privacy, and maintains image quality while enabling reliable identification based on the embedded signature.
    """,
    lifespan=lifespan,
    debug=settings.DEBUG,
)

add_cors_middleware(app)
include_routers(app)
add_exception_handlers(app)
