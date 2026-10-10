import logging

from fastapi import FastAPI

from app.config import Settings
from app.logging_config import configure_logging
from app.users.router import router as users_router

configure_logging()
logger = logging.getLogger(__name__)

settings = Settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(users_router)

logger.info("Application configured: %s", settings.app_name)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
