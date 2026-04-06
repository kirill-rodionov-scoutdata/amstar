from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ItemDTO(BaseModel):
    id: UUID
    title: str
    description: str | None
    created_at: datetime
