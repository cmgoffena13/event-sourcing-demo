from typing import Annotated

import structlog
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.settings import get_database_config

logger = structlog.get_logger(__name__)

db_config = get_database_config()

engine = create_engine(
    url=db_config["sqlalchemy.url"],
    echo=db_config["sqlalchemy.echo"],
    future=db_config["sqlalchemy.future"],
    connect_args=db_config.get("sqlalchemy.connect_args", {}),
    pool_size=db_config.get("sqlalchemy.pool_size", 20),
    max_overflow=db_config.get("sqlalchemy.max_overflow", 10),
    pool_timeout=db_config.get("sqlalchemy.pool_timeout", 30),
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_session():
    with SessionLocal() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
