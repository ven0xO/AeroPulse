import logging

from fastapi import FastAPI

from app.config import Settings
from app.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

settings = Settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)

logger.info("Application configured: %s", settings.app_name)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
