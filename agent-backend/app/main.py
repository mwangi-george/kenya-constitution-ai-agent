from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router
from app.core.config import settings
from app.db.initializer import DatabaseInitializer
from app.utils.splitter import split_comma_separated_variable


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize shared resources during app startup."""
    await DatabaseInitializer.initialize()
    yield


app = FastAPI(
    title=settings.app_name,
    root_path=settings.api_root_path,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=split_comma_separated_variable(settings.backend_cors_origins),
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
    max_age=86400
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Return a simple health status."""
    return {"status": "ok"}


app.include_router(chat_router)
