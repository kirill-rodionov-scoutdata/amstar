import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.domain.bookings.enums import BookingStatusEnum
from app.infra.db.mixins import IndexedTimeMixin, TimeMixin


class Base(DeclarativeBase):
    pass

_booking_status_enum = Enum(
    BookingStatusEnum,
    name="booking_status",
    values_callable=lambda e: [m.value for m in e],
)


class BookingORM(Base, IndexedTimeMixin):
    __tablename__ = "bookings"
    __table_args__ = (
        # Index 1: date-range listing query + optional status filter
        Index("idx_bookings_pickup_time_status", "pickup_time", "status"),
    )

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    passenger_name: Mapped[str] = mapped_column(String(100), nullable=False)
    flight_number: Mapped[str] = mapped_column(String(10), nullable=False)
    pickup_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    pickup_location: Mapped[str] = mapped_column(String(255), nullable=False)
    dropoff_location: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(
        _booking_status_enum,
        nullable=False,
        default=BookingStatusEnum.PENDING.value,
    )

    history: Mapped[list["BookingStatusHistoryORM"]] = relationship(
        "BookingStatusHistoryORM", back_populates="booking", cascade="all, delete-orphan"
    )
    notifications: Mapped[list["NotificationORM"]] = relationship(
        "NotificationORM", back_populates="booking", cascade="all, delete-orphan"
    )


class BookingStatusHistoryORM(Base):
    __tablename__ = "booking_status_history"
    __table_args__ = (
        # Index 2: history lookup by booking_id — MySQL does not auto-index FK columns
        Index("idx_booking_status_history_booking_id", "booking_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    booking_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    old_status: Mapped[str | None] = mapped_column(_booking_status_enum, nullable=True)
    new_status: Mapped[str] = mapped_column(_booking_status_enum, nullable=False)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    booking: Mapped["BookingORM"] = relationship("BookingORM", back_populates="history")


class NotificationORM(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    transfer_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    booking: Mapped["BookingORM"] = relationship("BookingORM", back_populates="notifications")
