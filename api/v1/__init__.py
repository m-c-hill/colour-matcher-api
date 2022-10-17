from fastapi import APIRouter

from .images import image_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(image_router)
