from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.app_layer.interfaces.services.items.create_item.dto import CreateItemRequest
from app.app_layer.interfaces.services.items.create_item.service import AbstractCreateItemService
from app.containers import Container
from app.domain.items.dto import ItemDTO

router = APIRouter()


@router.post("", response_model=ItemDTO, status_code=201)
@inject
async def create_item(
    data: CreateItemRequest,
    service: AbstractCreateItemService = Depends(Provide[Container.create_item_service]),
) -> ItemDTO:
    entity = await service.process(data)
    return entity.data
