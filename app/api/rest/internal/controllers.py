from fastapi import APIRouter

from app.api.rest.internal.v1.items.api import router as items_router

internal_router = APIRouter()

internal_router.include_router(items_router, prefix="/v1/items", tags=["items"])
