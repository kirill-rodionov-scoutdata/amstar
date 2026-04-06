from fastapi import APIRouter

from app.api.rest.internal.v1.bookings.api import router as bookings_router
from app.api.rest.internal.v1.items.api import router as items_router

internal_router = APIRouter()

internal_router.include_router(bookings_router, prefix="/v1/bookings", tags=["bookings"])
