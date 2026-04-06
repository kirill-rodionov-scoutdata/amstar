from app.domain.bookings.dto import BookingDTO
from app.domain.bookings.enums import BookingStatusEnum
from app.domain.bookings.exceptions import BookingCannotBeCancelledError, BookingInvalidTransitionError

_VALID_TRANSITIONS: dict[BookingStatusEnum, frozenset[BookingStatusEnum]] = {
    BookingStatusEnum.PENDING: frozenset({BookingStatusEnum.CONFIRMED, BookingStatusEnum.CANCELLED}),
    BookingStatusEnum.CONFIRMED: frozenset({BookingStatusEnum.IN_PROGRESS, BookingStatusEnum.CANCELLED}),
    BookingStatusEnum.IN_PROGRESS: frozenset({BookingStatusEnum.COMPLETED}),
    BookingStatusEnum.COMPLETED: frozenset(),
    BookingStatusEnum.CANCELLED: frozenset(),
}


class BookingEntity:
    def __init__(self, data: BookingDTO) -> None:
        self.data = data

    def cancel(self) -> None:
        if self.data.status not in (BookingStatusEnum.PENDING, BookingStatusEnum.CONFIRMED):
            raise BookingCannotBeCancelledError(
                f"Cannot cancel a booking with status '{self.data.status}'"
            )
        self.data.status = BookingStatusEnum.CANCELLED

    def transition_to(self, new_status: BookingStatusEnum) -> None:
        allowed = _VALID_TRANSITIONS.get(self.data.status, frozenset())
        if new_status not in allowed:
            raise BookingInvalidTransitionError(
                f"Cannot transition booking '{self.data.id}' "
                f"from '{self.data.status}' to '{new_status}'"
            )
        self.data.status = new_status
