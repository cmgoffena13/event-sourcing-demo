from contextlib import asynccontextmanager

from fastapi import FastAPI
from rich import panel

from src.app.types import ORJSONResponse
from src.logging_conf import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(panel.Panel("Server is starting up...", border_style="green"))
    setup_logging()
    yield
    print(panel.Panel("Server is shutting down...", border_style="red"))


app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)


@app.get("/")
async def root():
    return {"message": "Hello World"}
