from fastapi import FastAPI

from app.api.rest.internal.controllers import internal_router
from app.config import settings


def init_rest_api(app: FastAPI) -> None:
    app.include_router(internal_router, prefix=settings.API.INTERNAL_PREFIX)
