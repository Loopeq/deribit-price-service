from fastapi import APIRouter
from .prices import router as price_router

router = APIRouter(prefix="/v1")

router.include_router(price_router)
