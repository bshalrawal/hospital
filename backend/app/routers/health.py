from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/health", tags=["health"])


@router.get("", summary="Health check")
async def health_check() -> dict[str, str]:
    """Return basic service health information."""

    return {"status": "healthy"}
