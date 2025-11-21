import random
from datetime import datetime
from typing import Optional, TypedDict

from .configuracion import ConfigurarEstrellas
from .emocional import MotorEmocional
from .cliente import Cliente


class RespuestaSesion(TypedDict):
    texto: str
    modelo: str
    fecha: datetime


class ConsultasSesion(TypedDict):
    rol: str
    contenido: str
    instrucciones_internas: Optional[str]


class Sesion:
    def __init__(self):
        self.configuracion = ConfigurarEstrellas.get_instance()
        self._consultas: list[ConsultasSesion] = []
        # Se ve feo pero es necesario para inicializar la emoción correcta jaja
        if self.configuracion.configuracion_vidente.vidente == "lunita":
            self._emocion = MotorEmocional("data/emociones_lunita.json")
        elif self.configuracion.configuracion_vidente.vidente == "estrella":
            self._emocion = MotorEmocional("data/emociones_estrella.json")

        self.cliente = Cliente(
            emocion=self._emocion.obtener_para_prompt(),
        )

    async def predecir(self, pregunta: str) -> RespuestaSesion:
        """
        Simula una pregunta a la sesión de IA.
        """

        if random.random() < 0.15:
            self._emocion.obtener_nueva_emocion()
            self.cliente.actualizar_emocion(self._emocion.obtener_para_prompt())

        return {
            "texto": await self.cliente.preguntar(pregunta),
            "modelo": "modelo_simulado",
            "fecha": datetime.now(),
        }

    def cambiar_humor(self) -> str:
        """
        Cambia la emoción actual de la vidente. Todos podemos cambiar de humor incluso Lunita.

        Returns:
            str: La nueva emoción actual después del cambio.
        """
        self._emocion.obtener_nueva_emocion()
        return str(self._emocion.obtener_emocion())

    @property
    def consultas(self):
        """
        Obtiene el historial de consultas realizadas.
        """
        return self._consultas

    @consultas.setter
    def consultas(self, valor):
        """
        Establece un historial previo de consultas.
        """
        self._consultas = valor
