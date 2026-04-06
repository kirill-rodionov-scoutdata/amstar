from uuid import UUID

from pydantic import BaseModel, Field


class BatchUpdateStatusInputData(BaseModel):
    booking_ids: list[UUID] = Field(min_length=1, max_length=100)
    action: str
