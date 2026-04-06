from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from app.app_layer.providers.jwt import JwtProvider
from app.containers import Container


@inject
def get_jwt_provider(
    jwt_provider: JwtProvider = Depends(Provide[Container.jwt_provider]),
) -> JwtProvider:
    return jwt_provider
