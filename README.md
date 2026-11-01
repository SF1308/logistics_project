# Logistics Project

Aplicación web desarrollada con Django para gestionar órdenes de retiro de operadores logísticos.

## Requisitos

- Python
- PowerShell
- Git, si vas a clonar el repositorio

## Instalación y ejecución en Windows

Desde la carpeta del proyecto, ejecutá:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Configurá la clave requerida por Django para esta sesión de PowerShell:

```powershell
$env:DJANGO_SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Creá las tablas de la base de datos local y ejecutá el servidor:

```powershell
python manage.py migrate
python manage.py runserver
```

Abrí `http://127.0.0.1:8000/orders/` para acceder a la página de órdenes. La administración de Django está disponible en `http://127.0.0.1:8000/admin/`.

La base de datos SQLite se crea localmente. No se incluye en el repositorio.

## Confirmación de despacho

Permite confirmar el despacho de un envío desde la lista de envíos (`/envios/`) con el
botón "Confirmar despacho", o con un `POST` a:

```
POST /envios/<id>/despachar/
```

Confirmar un despacho es una única operación atómica: cambia el estado del envío a
`dispatched`, crea un `Movement` y registra una `DispatchConfirmation`. Si cualquier
paso falla, no se guarda nada.

### Respuestas

| Caso | Código | Cuerpo |
|---|---|---|
| Despacho confirmado | 200 | `{"envio", "estado_anterior", "estado_nuevo", "movimiento_creado", "confirmado": true}` |
| El envío no existe | 404 | `{"confirmado": false, "motivo": "..."}` |
| Regla de dominio (estado inválido, ya despachado) | 409 | `{"confirmado": false, "motivo": "..."}` |
| Fallo operativo (con rollback) | 500 | `{"confirmado": false, "motivo": "..."}` |

### Supuestos

- El flujo de estados es `pending → in_warehouse → dispatched → out_for_delivery → delivered / failed`.
  Se agregó `dispatched` porque el enunciado habla de "marcar un envío como despachado".
- Solo se puede despachar un envío que está en `in_warehouse`. Las reglas están en
  `DISPATCHABLE_FROM`, en `shipments/services.py`.
- Un envío ya despachado se rechaza (409), no se ignora en silencio.
- La "constancia persistente" es un modelo aparte (`DispatchConfirmation`) con relación
  uno a uno con el envío, para que la base de datos impida una doble confirmación.
- No hay usuarios en el proyecto, por eso `confirmed_by` queda vacío; el campo está
  preparado para cuando haya autenticación.
- La respuesta es JSON, porque el ejercicio define así su resultado esperado.
- El botón se muestra en todos los envíos: la regla de qué se puede despachar vive solo
  en el servicio, y la interfaz muestra el motivo cuando el servicio rechaza.
- No se desactiva la protección CSRF: el botón envía el token. Para probar con
  Postman o curl hay que enviar el header `X-CSRFToken`.
- `select_for_update` evita confirmaciones concurrentes en PostgreSQL o MySQL; SQLite
  lo ignora, y ahí la protección final es la relación uno a uno.

## Dependencias

Las dependencias de Python están declaradas en `requirements.txt`.
