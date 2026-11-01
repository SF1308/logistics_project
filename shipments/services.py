import logging

from django.db import transaction
from django.utils import timezone

from dataclasses import dataclass

from .models import DispatchConfirmation, Movement, Shipment
from .models import Shipment

# Reglas de negocio, en un solo lugar.
DISPATCHED_STATUS = Shipment.Status.DISPATCHED
DISPATCHABLE_FROM = {Shipment.Status.IN_WAREHOUSE}

logger = logging.getLogger(__name__)


class DispatchError(Exception):
    """Base: cualquier caso en que el despacho NO se confirmó."""


class ShipmentNotFound(DispatchError):
    """El envío no existe."""


class InvalidShipmentState(DispatchError):
    """Una regla de dominio rechazó la confirmación."""


class DispatchFailed(DispatchError):
    """Falló algo operativo; se revirtió todo."""


@dataclass(frozen=True)
class DispatchResult:
    shipment_code: str
    previous_status: str
    new_status: str
    movement_id: int


def confirm_dispatch(shipment_id, confirmed_by=""):
    try:
        with transaction.atomic():
            shipment = (
                Shipment.objects.select_for_update().filter(pk=shipment_id).first()
            )
            if shipment is None:
                raise ShipmentNotFound("El envío no existe.")

            if shipment.status not in DISPATCHABLE_FROM:
                raise InvalidShipmentState("Solo se puede confirmar el despacho de envíos que están en depósito.")

            previous_status = shipment.status
            confirmed_at = timezone.now()

            shipment.status = DISPATCHED_STATUS
            shipment.save(update_fields=["status"])

            movement = Movement.objects.create(
                shipment=shipment,
                status=DISPATCHED_STATUS,
                description="Despacho confirmado.",
                occurred_at=confirmed_at,
            )

            DispatchConfirmation.objects.create(
                shipment=shipment,
                confirmed_at=confirmed_at,
                confirmed_by=confirmed_by,
            )

            return DispatchResult(
                shipment_code=shipment.code,
                previous_status=previous_status,
                new_status=shipment.status,
                movement_id=movement.id,
            )
    except DispatchError:
        raise
    except Exception as exc:
        logger.exception("Falló la confirmación del despacho del envío %s", shipment_id)
        raise DispatchFailed("No se pudo confirmar el despacho.") from exc
