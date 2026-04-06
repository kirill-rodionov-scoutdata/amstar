class CreateBookingError(Exception):
    pass


class BookingValidationError(CreateBookingError):
    pass


class BookingFlightNotFoundError(CreateBookingError):
    pass


class BookingUnauthorizedError(CreateBookingError):
    pass
