from fastapi import APIRouter, FastAPI

from src.controllers.api import auth_controller, user_controller, stego_controller

def include_routers(app: FastAPI) -> None:
    api_router = APIRouter(prefix="/api")
    api_router.include_router(auth_controller.router)
    api_router.include_router(user_controller.router)
    api_router.include_router(stego_controller.router)
    # Add other routers here as needed
    
    app.include_router(api_router)
