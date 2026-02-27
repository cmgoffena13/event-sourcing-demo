import os
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from src.database.session import engine
from src.logging_conf import setup_logging
from src.routes.main import router as main_router
from src.settings import config
from src.types import ORJSONResponse

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Starting server...")
    os.environ["PERSISTENCE_MODULE"] = "eventsourcing_sqlalchemy"
    os.environ["SQLALCHEMY_URL"] = config.DATABASE_URL

    yield

    logger.info("Shutting down server...")
    engine.dispose()


app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)

app.include_router(main_router)


@app.get("/scalar", include_in_schema=False)
async def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
