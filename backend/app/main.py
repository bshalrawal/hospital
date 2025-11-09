from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import health

app = FastAPI(title=settings.app_name, version="0.1.0")

origins = (
    [settings.backend_cors_origins]
    if isinstance(settings.backend_cors_origins, str)
    else settings.backend_cors_origins
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)


@app.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    """Simple root endpoint to verify service availability."""

    return {"message": "Hospital Equipment Management API"}
