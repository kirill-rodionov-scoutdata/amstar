from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.domain.bookings.enums import BookingStatusEnum


class BookingDTO(BaseModel):
    id: UUID
    passenger_name: str
    flight_number: str
    pickup_time: datetime
    pickup_location: str
    dropoff_location: str
    status: BookingStatusEnum
    created_at: datetime
