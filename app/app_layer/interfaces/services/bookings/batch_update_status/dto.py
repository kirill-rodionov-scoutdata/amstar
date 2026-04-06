from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.bookings.enums import BookingStatusEnum


class BatchUpdateStatusRequest(BaseModel):
    booking_ids: list[UUID] = Field(min_length=1, max_length=100)
    new_status: BookingStatusEnum
