import os
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from src.database.session import engine
from src.logging_conf import setup_logging
from src.settings import config
from src.types import ORJSONResponse

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Starting server...")
    os.environ["PERSISTENCE_MODULE"] = "eventsourcing_sqlalchemy"
    os.environ["SQLALCHEMY_DATABASE_URL"] = config.DATABASE_URL

    yield

    logger.info("Shutting down server...")
    await engine.dispose()


app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)


@app.get("/")
async def heartbeat():
    return {"status": "ok"}
