from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.database.health import check_database

router = APIRouter(prefix="/health",tags=["Health"])

@router.get("/")
def health(db: Session = Depends(get_db)):
    return{
        "application": "BusinessPilot AI",
        "database": check_database(db),
        "status":"healthy",
    }