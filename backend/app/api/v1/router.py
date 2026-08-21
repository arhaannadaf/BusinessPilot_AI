from fastapi import APIRouter

from app.api.monitoring_router import router as monitoring_router


router = APIRouter()

router.include_router(monitoring_router)