from fastapi import FastAPI
from app.core.config.settings import settings
from app.shared.logging import logger
from app.api.router import router
from app.core.exceptions import generic_exception_handler 

logger.info("BusinessPilot AI started")
app = FastAPI(
    title="BusinessPilot AI API",
    description="Enterprise Decision Intelligence System",
    version="0.1.0",
)

app.include_router(router,prefix="/api")
app.add_exception_handler(Exception,generic_exception_handler)
@app.get("/")
async def root():
    return {
        "application": settings.app_name,
        "version" : settings.app_version,
        "status" : "running",
    }