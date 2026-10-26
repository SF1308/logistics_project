from django.contrib import admin

from .models import Company, Movement, Shipment


class MovementInline(admin.TabularInline):
    model = Movement
    extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("code", "company", "status", "priority", "created_at")
    list_filter = ("company", "status", "priority")
    inlines = [MovementInline]
