from django.shortcuts import redirect, render

from .models import Order
from .services import create_order


def order_page(request):
    values = {}
    errors = {}

    if request.method == "POST":
        order, errors = create_order(request.POST)

        if not errors:
            return redirect("orders:order_page")

        values = request.POST

    orders = Order.objects.order_by("-created_at")

    return render(
        request,
        "orders/order_page.html",
        {
            "values": values,
            "errors": errors,
            "orders": orders,
        },
    )
