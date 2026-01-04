from fastapi import APIRouter
from src.routes import user_router, dev_router

router = APIRouter()

router.include_router(user_router)
router.include_router(dev_router)
