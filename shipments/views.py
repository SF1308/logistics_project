from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

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
