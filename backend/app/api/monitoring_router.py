from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.database.health import check_database

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health(
    db: AsyncSession = Depends(get_db),
):
    return {
        "application": "BusinessPilot AI",
        "database": await check_database(db),
        "status": "healthy",
    }