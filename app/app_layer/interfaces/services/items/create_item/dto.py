from pydantic import BaseModel


class CreateItemRequest(BaseModel):
    title: str
    description: str | None = None
