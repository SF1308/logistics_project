from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name


class Shipment(models.Model):
    class Priority(models.IntegerChoices):
        # Lower number = more urgent, so it can be ordered directly in the database.
        HIGH = 1, "Alta"
        MEDIUM = 2, "Media"
        LOW = 3, "Baja"

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        IN_WAREHOUSE = "in_warehouse", "En depósito"
        OUT_FOR_DELIVERY = "out_for_delivery", "En reparto"
        DELIVERED = "delivered", "Entregado"
        FAILED = "failed", "Entrega fallida"

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="shipments",
    )
    code = models.CharField(max_length=50)
    recipient = models.CharField(max_length=200)
    destination_address = models.CharField(max_length=300)
    priority = models.PositiveSmallIntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "code"],
                name="unique_shipment_code_per_company",
            ),
        ]

    def __str__(self):
        return f"{self.code} ({self.company})"


class Movement(models.Model):
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="movements",
    )
    status = models.CharField(max_length=20, choices=Shipment.Status.choices)
    description = models.CharField(max_length=300, blank=True)
    occurred_at = models.DateTimeField()

    def __str__(self):
        return f"{self.shipment.code}: {self.get_status_display()}"
