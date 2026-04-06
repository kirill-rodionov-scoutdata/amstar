class BatchUpdateStatusError(Exception):
    pass


class BatchBookingNotFoundError(BatchUpdateStatusError):
    def __init__(self, missing_ids: list[str]) -> None:
        self.missing_ids = missing_ids
        super().__init__(f"Bookings not found: {missing_ids}")


class BatchInvalidTransitionError(BatchUpdateStatusError):
    def __init__(self, booking_id: str, from_status: str, to_status: str) -> None:
        self.booking_id = booking_id
        self.from_status = from_status
        self.to_status = to_status
        super().__init__(
            f"Invalid transition for booking '{booking_id}': '{from_status}' -> '{to_status}'"
        )
