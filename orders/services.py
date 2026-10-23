from .models import Order


def create_order(data):
    requester = data.get("requester", "").strip()
    internal_id = data.get("internal_id", "").strip()
    service_type = data.get("service_type", "").strip()
    package_count_value = data.get("package_count", "").strip()
    notes = data.get("notes", "").strip()

    errors = {}

    if not requester:
        errors["requester"] = "Indica quién solicita el retiro."
    elif len(requester) > 200:
        errors["requester"] = "No puede superar los 200 caracteres."

    if not internal_id:
        errors["internal_id"] = "Indica el identificador interno."
    elif len(internal_id) > 100:
        errors["internal_id"] = "No puede superar los 100 caracteres."

    if not service_type:
        errors["service_type"] = "Indica el tipo de servicio."
    elif len(service_type) > 100:
        errors["service_type"] = "No puede superar los 100 caracteres."

    try:
        package_count = int(package_count_value)
        if package_count <= 0:
            errors["package_count"] = "La cantidad debe ser mayor que cero."
    except ValueError:
        errors["package_count"] = "Indica una cantidad válida de bultos."

    if errors:
        return None, errors

    order = Order.objects.create(
        requester=requester,
        internal_id=internal_id,
        service_type=service_type,
        package_count=package_count,
        notes=notes,
    )

    return order, {}
