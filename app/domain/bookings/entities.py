from app.domain.bookings.dto import BookingDTO
from app.domain.bookings.enums import BookingStatusEnum
from app.domain.bookings.exceptions import BookingCannotBeCancelledError


class BookingEntity:
    def __init__(self, data: BookingDTO) -> None:
        self.data = data

    def cancel(self) -> None:
        if self.data.status not in (BookingStatusEnum.PENDING, BookingStatusEnum.CONFIRMED):
            raise BookingCannotBeCancelledError(
                f"Cannot cancel a booking with status '{self.data.status}'"
            )
        self.data.status = BookingStatusEnum.CANCELLED
