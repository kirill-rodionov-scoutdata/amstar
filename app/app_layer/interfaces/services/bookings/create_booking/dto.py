from datetime import UTC, datetime

from pydantic import BaseModel, Field, field_validator, model_validator


class CreateBookingRequest(BaseModel):
    passenger_name: str = Field(min_length=2, max_length=100)
    flight_number: str = Field(pattern=r"^[A-Z]{2,3}\d{1,4}$")
    pickup_time: datetime
    pickup_location: str = Field(min_length=2, max_length=255)
    dropoff_location: str = Field(min_length=2, max_length=255)

    @field_validator("pickup_time")
    @classmethod
    def pickup_time_must_be_future(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("pickup_time must be timezone-aware")
        if v <= datetime.now(UTC):
            raise ValueError("pickup_time must be in the future")
        return v

    @model_validator(mode="after")
    def locations_must_differ(self) -> "CreateBookingRequest":
        if self.pickup_location == self.dropoff_location:
            raise ValueError("pickup_location and dropoff_location must differ")
        return self
