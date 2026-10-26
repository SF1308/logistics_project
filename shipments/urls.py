from django.urls import path

from . import views

app_name = "shipments"

urlpatterns = [
    path("envios/", views.shipment_list, name="shipment_list"),
]
