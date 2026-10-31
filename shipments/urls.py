from django.urls import path

from . import views

app_name = "shipments"

urlpatterns = [
    path("envios/", views.shipment_list, name="shipment_list"),
    path("envios/<int:company_id>/", views.shipment_list_by_company, name="shipment_list_by_company"),
]
