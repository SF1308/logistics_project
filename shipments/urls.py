from django.urls import path

from . import views

app_name = "shipments"

urlpatterns = [
    path("envios/", views.shipment_list, name="shipment_list"),
    path("envios/<int:company_id>/", views.shipment_list_by_company, name="shipment_list_by_company"),
    path("envios/<int:shipment_id>/despachar/",views.confirm_shipment_dispatch, name="confirm_dispatch",),
    path("tablero/", views.active_shipments_board, name="active_board"),
]
