import pytest
from pydantic import ValidationError

from app.app_layer.interfaces.services.bookings.create_one.dto import CreateBookingInputData


def test_valid_payload_passes(load_json_data) -> None:
    cases = load_json_data("create_booking_valid.json")
    for case in cases:
        result = CreateBookingInputData(**case)
        assert result.passenger_name == case["passenger_name"]


def test_invalid_payload_raises_validation_error(load_json_data) -> None:
    data = load_json_data("create_booking_invalid.json")
    for entry in data:
        payload = entry["payload"]
        with pytest.raises(ValidationError):
            CreateBookingInputData(**payload)
