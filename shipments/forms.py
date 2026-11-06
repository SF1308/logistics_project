from django import forms

from .models import Company, Shipment

DEFAULT_ORDER = "urgencia"

ORDERINGS = {
    "urgencia": ("priority", "created_at", "id"),
    "antiguos": ("created_at", "id"),
    "recientes": ("-created_at", "-id"),
}

ORDER_CHOICES = [
    ("urgencia", "Más urgentes primero"),
    ("antiguos", "Más antiguos primero"),
    ("recientes", "Más recientes primero"),
]

ACTIVE_STATUS_CHOICES = [("", "Todos los activos")] + [
    (status.value, status.label) for status in Shipment.ACTIVE_STATUSES
]


class BoardFilterForm(forms.Form):
    desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
    )
    hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
    )
    estado = forms.ChoiceField(
        label="Estado", required=False, choices=ACTIVE_STATUS_CHOICES
    )
    empresa = forms.ModelChoiceField(
        label="Empresa",
        required=False,
        queryset=Company.objects.all(),
        empty_label="Todas",
    )
    orden = forms.ChoiceField(
        label="Orden", required=False, choices=ORDER_CHOICES
    )

    def clean(self):
        cleaned = super().clean()
        desde, hasta = cleaned.get("desde"), cleaned.get("hasta")
        if desde and hasta and desde > hasta:
            raise forms.ValidationError(
                "La fecha “desde” no puede ser posterior a “hasta”."
            )
        return cleaned

    def get_ordering(self):
        key = getattr(self, "cleaned_data", {}).get("orden") or DEFAULT_ORDER
        return ORDERINGS[key]
