import logging
import random
from typing import TypedDict

from .utilidades import CargadorDatos

logger = logging.getLogger(__name__)


class EstadoEmocional(TypedDict):
    situacion: str
    emociones: list[str]


class MotorEmocional(CargadorDatos):
    """
    NAME
        MotorEmocional - Gestiona el estado emocional de Lunita.

    SYNOPSIS
        - me = MotorEmocional(ruta)
        - me.obtener_emocion() -> str
        - me.obtener_nueva_emocion() -> str

    DESCRIPTION
        Hereda de `CargadorDatos` para cargar una lista de emociones desde un archivo
        JSON y proporciona métodos para obtener una emoción aleatoria, ya sea la
        actual o una nueva.

    ATTRIBUTES
        emocion_actual : int
            Índice numérico que representa la emoción actual en la lista de emociones.
    """

    def __init__(self, ruta: str) -> None:
        """Inicializa el motor emocional.

        DESCRIPTION
            Llama al constructor de la clase base con la ruta del archivo y establece
            un estado de ánimo inicial seleccionando un índice aleatorio de la lista
            de emociones cargada.

        PARAMETERS
            ruta
                Ruta al archivo JSON que contiene la lista de emociones.
        """
        super().__init__(ruta=ruta)
        self.emocion_actual = random.randint(0, len(self.cargar_datos()) - 1)
        logger.info(
            f"Motor emocional inicializado con emoción: {self.obtener_emocion()}"
        )

    def obtener_emocion(self) -> EstadoEmocional:
        """Obtiene la emoción actual.

        RETURN VALUES
            str
                La cadena de texto que representa la emoción actual.
        """
        return self.cargar_datos()[self.emocion_actual]

    def obtener_situacion(self) -> str:
        return self.obtener_emocion()["situacion"]

    def obtener_emociones(self) -> list[str]:
        return self.obtener_emocion()["emociones"]

    def obtener_para_prompt(self) -> str:
        """Formato limpio para incluir en el system prompt"""
        emociones_str = ", ".join(self.obtener_emociones())

        return f"""Situación: {self.obtener_situacion()}
Sentimientos: {emociones_str}

Incorpora sutilmente esta situación en tu comportamiento cuando sea natural."""

    def obtener_nueva_emocion(self) -> EstadoEmocional:
        """Selecciona y devuelve una nueva emoción aleatoria.

        SIDE EFFECTS
            Modifica el atributo `self.emocion_actual` a un nuevo valor aleatorio.

        RETURN VALUES
            str
                La cadena de texto de la nueva emoción seleccionada.
        """
        emociones = self.cargar_datos()
        if not emociones:
            return {
                "situacion": "curiosa por los astros",
                "emociones": ["curiosidad", "asombro"],
            }

        nueva_emocion = self.emocion_actual
        intentos = 0
        while nueva_emocion == self.emocion_actual and intentos < 10:
            nueva_emocion = random.randint(0, len(emociones) - 1)
            intentos += 1

        self.emocion_actual = nueva_emocion
        emocion_texto = self.obtener_emocion()
        logger.info(f"Emoción cambiada a: {emocion_texto}")
        return emocion_texto

    def establecer_emocion_especifica(self, emocion: str) -> bool:
        """Establece una emoción específica si existe en la lista"""
        emociones = self.cargar_datos()
        try:
            indice = emociones.index(emocion)  # type: ignore
            self.emocion_actual = indice
            logger.info(f"Emoción cambiada a: {emocion}")
            return True
        except ValueError:
            logger.error(f"Emoción {emocion} no encontrada")
            return False
