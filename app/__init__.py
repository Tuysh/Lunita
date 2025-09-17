"""
NAME
    app - Paquete principal de la aplicación Lunita.

DESCRIPTION
    Este paquete contiene toda la lógica de la aplicación, incluyendo el cliente de la API,
    el motor emocional, la moderación y la clase principal `Lunita`.

    Este archivo `__init__.py` expone la clase `Lunita` como la interfaz pública
    principal del paquete, permitiendo su importación directa desde `app`.
"""

from .lunita import Lunita

__all__ = ["Lunita"]
