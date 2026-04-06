from datetime import UTC, datetime

from app.app_layer.interfaces.services.bookings.patch_update.dto import BatchUpdateStatusRequest
from app.app_layer.interfaces.services.bookings.patch_update.exceptions import (
    BatchBookingNotFoundError,
    BatchInvalidTransitionError,
)
from app.app_layer.interfaces.services.bookings.patch_update.service import AbstractBatchUpdateStatusService
from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork
from app.domain.bookings.entities import BookingEntity
from app.domain.bookings.enums import BookingStatusEnum
from app.domain.bookings.exceptions import BookingInvalidTransitionError


class BatchUpdateStatusService(AbstractBatchUpdateStatusService):
    def __init__(self, uow: AbcUnitOfWork) -> None:
        self.uow = uow

    async def process(self, data: BatchUpdateStatusRequest) -> list[BookingEntity]:
        async with self.uow as uow:
            # Phase 1: fetch all — fail fast if any are missing
            entities = await uow.booking_repo.get_by_ids(data.booking_ids)
            fetched_ids = {entity.data.id for entity in entities}
            missing = [bid for bid in data.booking_ids if bid not in fetched_ids]
            if missing:
                raise BatchBookingNotFoundError([str(m) for m in missing])

            # Phase 2+3: validate transition, persist update + history + notification
            now = datetime.now(UTC)
            updated: list[BookingEntity] = []

            for entity in entities:
                old_status = entity.data.status  # capture before mutation
                try:
                    entity.transition_to(data.new_status)
                except BookingInvalidTransitionError:
                    raise BatchInvalidTransitionError(
                        booking_id=str(entity.data.id),
                        from_status=old_status.value,
                        to_status=data.new_status.value,
                    )

                updated_entity = await uow.booking_repo.update_status(entity.data.id, entity.data.status)
                await uow.booking_repo.create_status_history(
                    booking_id=entity.data.id,
                    old_status=old_status,
                    new_status=entity.data.status,
                    changed_at=now,
                )
                if entity.data.status == BookingStatusEnum.CONFIRMED:
                    await uow.booking_repo.create_notification(
                        booking_id=entity.data.id,
                        message=f"Your booking {entity.data.id} has been confirmed.",
                        sent_at=now,
                    )
                updated.append(updated_entity)

        return updated
