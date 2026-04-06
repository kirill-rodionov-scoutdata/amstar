from datetime import datetime
from pydantic import BaseModel

from app.domain.bookings.enums import BookingStatusEnum


class BookingStatusHistoryDTO(BaseModel):
    old_status: BookingStatusEnum
    new_status: BookingStatusEnum
    changed_at: datetime
