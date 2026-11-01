from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from .services import (
    DispatchFailed,
    InvalidShipmentState,
    ShipmentNotFound,
    confirm_dispatch,
)

from .models import Company, Shipment


@require_GET
def shipment_list(request):
    # company_id = request.GET.get("empresa_id", "")

    # if not company_id.isdigit():
    #     return HttpResponseBadRequest("empresa_id debe ser un número entero.")

    # company = get_object_or_404(Company, pk=int(company_id))

    # Filtering and ordering happen in the database:
    # most urgent first, then oldest first (id breaks ties).
    shipments = Shipment.objects.all().order_by(
        "priority", "created_at", "id"
    )

    return render(
        request,
        "shipments/shipment_list.html",
        {
            "shipments": shipments,
        },
    )

@require_GET
def shipment_list_by_company(request):
    company_id = request.GET.get("empresa_id", "")

    if not company_id.isdigit():
        return HttpResponseBadRequest("empresa_id debe ser un número entero.")

    company = get_object_or_404(Company, pk=int(company_id))

    # Filtering and ordering happen in the database:
    # most urgent first, then oldest first (id breaks ties).
    shipments = Shipment.objects.filter(company=company).order_by(
        "priority", "created_at", "id"
    )

    return render(
        request,
        "shipments/shipment_list.html",
        {
            "company": company,
            "shipments": shipments,
        },
    )

@require_POST
def confirm_shipment_dispatch(request, shipment_id):
    try:
        result = confirm_dispatch(shipment_id)
        print(f"Despacho confirmado: {result.shipment_code} (movimiento {result.movement_id})")
    except ShipmentNotFound as exc:
        return JsonResponse({"confirmado": False, "motivo": str(exc)}, status=404)
    except InvalidShipmentState as exc:
        return JsonResponse({"confirmado": False, "motivo": str(exc)}, status=409)
    except DispatchFailed as exc:
        return JsonResponse({"confirmado": False, "motivo": str(exc)}, status=500)

    return JsonResponse(
        {
            "envio": result.shipment_code,
            "estado_anterior": result.previous_status,
            "estado_nuevo": result.new_status,
            "movimiento_creado": result.movement_id,
            "confirmado": True,
        }
    )
