import random
from datetime import datetime
from typing import Optional, TypedDict

from .cliente import Cliente
from .configuracion import ConfigurarEstrellas
from .emocional import MotorEmocional
from .memoria import MemoriaDia


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
            self._recuerdo = MemoriaDia("data/recuerdos_lunita.json")
        elif self.configuracion.configuracion_vidente.vidente == "estrella":
            self._recuerdo = MemoriaDia("data/recuerdos_estrella.json")

        self._emociones = MotorEmocional("data/emociones_lunita.json")

        self.cliente = Cliente(
            emocion=self._recuerdo.obtener_para_prompt(),
        )

    async def predecir(self, pregunta: str) -> RespuestaSesion:
        """
        Simula una pregunta a la sesión de IA.
        """

        cambio_forzado = self._emociones.analizar_vibe_usuario(pregunta)

        if not cambio_forzado and random.random() < 0.15:
            self._emociones.obtener_nueva_emocion_al_azar()

        print(
            f"[DEBUG] Emoción actual después de analizar: {self._emociones.obtener_estado_actual()}"
        )

        prompt_emociones = f"{self._recuerdo.obtener_recuerdo_completo()}\nEMOCIONES ACTUALES: {self._emociones.obtener_estado_actual_prompt()}"

        # 3. Actualizamos el prompt del sistema con la emoción final
        self.cliente.actualizar_emocion(prompt_emociones)

        return {
            "texto": await self.cliente.preguntar(pregunta),
            "modelo": self.configuracion.modelo,
            "fecha": datetime.now(),
        }

    def cambiar_humor(self) -> str:
        """
        Cambia la emoción actual de la vidente. Todos podemos cambiar de humor incluso Lunita.

        Returns:
            str: La nueva emoción actual después del cambio.
        """
        self._emociones.obtener_nueva_emocion_al_azar()
        return str(self._emociones.obtener_estado_actual())

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
