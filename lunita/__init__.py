"""
NAME
    lunita - Paquete principal de la aplicación Lunita.

DESCRIPTION
    Este paquete contiene toda la lógica de la aplicación, incluyendo el cliente de la API,
    el motor emocional, la moderación y la clase principal `Lunita`.

    Este archivo `__init__.py` expone la clase `Lunita` como la interfaz pública
    principal del paquete, permitiendo su importación directa desde `lunita`.
"""

from .sesion import Sesion
from .configuracion import ConfigurarEstrellas
from .vidente import ConfigurarVidente

__all__ = ["Sesion", "ConfigurarEstrellas", "ConfigurarVidente"]
