class BookingNotFoundError(Exception):
    pass


class BookingCannotBeCancelledError(Exception):
    pass


class BookingInvalidTransitionError(Exception):
    pass
