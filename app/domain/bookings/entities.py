from app.domain.bookings.dto import BookingDTO


class BookingEntity:
    def __init__(self, data: BookingDTO) -> None:
        self.data = data
