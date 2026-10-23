from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"

    requester = models.CharField(max_length=200)
    internal_id = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    package_count = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.internal_id} - {self.requester}"
