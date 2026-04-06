import uuid

from sqlalchemy import String, Text
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.infra.db.mixins import TimeMixin


class Base(DeclarativeBase):
    pass


class ItemORM(Base, TimeMixin):
    __tablename__ = "items"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
