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

## Dependencias

Las dependencias de Python están declaradas en `requirements.txt`.
