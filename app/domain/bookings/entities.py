from app.domain.bookings.dto import BookingDTO
from app.domain.bookings.enums import BookingStatusEnum
from app.domain.bookings.exceptions import BookingCannotBeCancelledError, BookingInvalidTransitionError


class BookingEntity:
    def __init__(self, data: BookingDTO) -> None:
        self.data = data

    def cancel(self) -> None:
        if self.data.status not in (BookingStatusEnum.PENDING, BookingStatusEnum.CONFIRMED):
            raise BookingCannotBeCancelledError(
                f"Cannot cancel a booking with status '{self.data.status}'"
            )
        self.data.status = BookingStatusEnum.CANCELLED

    def go_next(self) -> None:
        if self.data.status == BookingStatusEnum.PENDING:
            self.data.status = BookingStatusEnum.CONFIRMED
            return

        if self.data.status == BookingStatusEnum.CONFIRMED:
            self.data.status = BookingStatusEnum.IN_PROGRESS
            return

        if self.data.status == BookingStatusEnum.IN_PROGRESS:
            self.data.status = BookingStatusEnum.COMPLETED
            return

        raise BookingInvalidTransitionError(
            f"No next step from '{self.data.status}'"
        )
