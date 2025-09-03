from fastapi import APIRouter
from src.api.endpoints import router as api_router

main_router = APIRouter()
main_router.include_router(api_router)
