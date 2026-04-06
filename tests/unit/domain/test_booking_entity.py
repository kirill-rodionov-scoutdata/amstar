import pytest

from app.domain.bookings.enums import BookingStatusEnum
from app.domain.bookings.exceptions import BookingCannotBeCancelledError, BookingInvalidTransitionError


def test_cancel_from_pending_sets_cancelled(booking_entity_factory) -> None:
    entity = booking_entity_factory(status=BookingStatusEnum.PENDING)
    entity.cancel()
    assert entity.data.status == BookingStatusEnum.CANCELLED


def test_cancel_from_confirmed_sets_cancelled(booking_entity_factory) -> None:
    entity = booking_entity_factory(status=BookingStatusEnum.CONFIRMED)
    entity.cancel()
    assert entity.data.status == BookingStatusEnum.CANCELLED


def test_cancel_from_in_progress_raises(booking_entity_factory) -> None:
    entity = booking_entity_factory(status=BookingStatusEnum.IN_PROGRESS)
    with pytest.raises(BookingCannotBeCancelledError):
        entity.cancel()


def test_cancel_from_completed_raises(booking_entity_factory) -> None:
    entity = booking_entity_factory(status=BookingStatusEnum.COMPLETED)
    with pytest.raises(BookingCannotBeCancelledError):
        entity.cancel()


def test_cancel_from_cancelled_raises(booking_entity_factory) -> None:
    entity = booking_entity_factory(status=BookingStatusEnum.CANCELLED)
    with pytest.raises(BookingCannotBeCancelledError):
        entity.cancel()


def test_go_next_pending_to_confirmed(booking_entity_factory) -> None:
    entity = booking_entity_factory(status=BookingStatusEnum.PENDING)
    entity.go_next()
    assert entity.data.status == BookingStatusEnum.CONFIRMED


def test_go_next_confirmed_to_in_progress(booking_entity_factory) -> None:
    entity = booking_entity_factory(status=BookingStatusEnum.CONFIRMED)
    entity.go_next()
    assert entity.data.status == BookingStatusEnum.IN_PROGRESS


def test_go_next_in_progress_to_completed(booking_entity_factory) -> None:
    entity = booking_entity_factory(status=BookingStatusEnum.IN_PROGRESS)
    entity.go_next()
    assert entity.data.status == BookingStatusEnum.COMPLETED


def test_go_next_from_completed_raises(booking_entity_factory) -> None:
    entity = booking_entity_factory(status=BookingStatusEnum.COMPLETED)
    with pytest.raises(BookingInvalidTransitionError):
        entity.go_next()


def test_go_next_from_cancelled_raises(booking_entity_factory) -> None:
    entity = booking_entity_factory(status=BookingStatusEnum.CANCELLED)
    with pytest.raises(BookingInvalidTransitionError):
        entity.go_next()
