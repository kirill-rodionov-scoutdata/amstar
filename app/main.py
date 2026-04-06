from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.rest.controllers import init_rest_api
from app.config import settings
from app.containers import Container


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()
    container.wire(
        packages=[
            "app.api",
            "app.app_layer",
            "app.dependencies",
        ]
    )
    app.state.container = container
    await container.init_resources()
    yield
    await container.shutdown_resources()


def create_app() -> FastAPI:
    docs_url = "/docs" if settings.API.DOCS_ENABLED else None
    redoc_url = "/redoc" if settings.API.DOCS_ENABLED else None

    app = FastAPI(
        title=settings.DB.APP_NAME,
        version=settings.API.DOCS_VERSION,
        lifespan=lifespan,
        docs_url=docs_url,
        redoc_url=redoc_url,
    )

    init_rest_api(app)

    return app


app = create_app()
