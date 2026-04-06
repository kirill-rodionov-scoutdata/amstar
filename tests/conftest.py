import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork
from app.domain.bookings.dto import BookingDTO
from app.domain.bookings.entities import BookingEntity
from app.domain.bookings.enums import BookingStatusEnum
from app.main import create_app


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return create_app()


@pytest.fixture
async def base_client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
def booking_entity_factory():
    def _make_entity(
        status: BookingStatusEnum = BookingStatusEnum.PENDING,
        passenger_name: str = "Test Passenger",
        flight_number: str = "TP1234",
    ) -> BookingEntity:
        dto = BookingDTO(
            id=uuid.uuid4(),
            passenger_name=passenger_name,
            flight_number=flight_number,
            pickup_time=datetime(2027, 5, 10, 8, 0, tzinfo=timezone.utc),
            pickup_location="Pickup Location",
            dropoff_location="Dropoff Location",
            status=status,
            created_at=datetime(2027, 1, 1, tzinfo=timezone.utc),
        )
        return BookingEntity(data=dto)

    return _make_entity


@pytest.fixture
def mock_booking_repo():
    repo = MagicMock()
    repo.create = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_ids = AsyncMock()
    repo.update_status = AsyncMock()
    repo.create_status_history = AsyncMock()
    return repo


@pytest.fixture
def mock_uow(mock_booking_repo):
    uow = MagicMock(spec=AbcUnitOfWork)
    uow.booking_repo = mock_booking_repo
    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=None)
    uow.commit = AsyncMock()
    uow.rollback = AsyncMock()
    return uow


@pytest.fixture
def load_json_data():
    import json
    from pathlib import Path

    def _load(filename: str) -> dict | list:
        # Assumes the tests directory is the parent of this conftest.py
        path = Path(__file__).parent / "data" / filename
        with path.open() as f:
            return json.load(f)

    return _load
