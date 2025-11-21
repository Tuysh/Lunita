from typing import Optional

from pydantic import TypeAdapter
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage

from .configuracion import ConfigurarEstrellas
from .constantes import AJUSTES_CONTEXTO, PROMPT_ESTRELLA, PROMPT_LUNITA
from .herramientas import HERRAMIENTAS

AdaptadorMensajes = TypeAdapter(list[ModelMessage])


class Cliente:
    def __init__(
        self,
        emocion: str,
        historial: Optional[list[ModelMessage]] = None,
    ):
        self.configuracion = ConfigurarEstrellas.get_instance()
        self.emocion = emocion
        self.historial: list[ModelMessage] = historial or []
        self._agente = self._crear_agente()

    def _crear_agente(self) -> Agent:
        return Agent(
            model=self.configuracion.configuracion_modelo(),
            tools=HERRAMIENTAS,
            system_prompt=self._construir_prompt_sistema(),
        )

    def _construir_prompt_sistema(self) -> str:
        """Construye el prompt del sistema con la emoción actual"""
        prompt = (
            PROMPT_LUNITA
            if self.configuracion.configuracion_vidente.vidente == "lunita"
            else PROMPT_ESTRELLA
        )
        prompt += f"\nESTADO EMOCIONAL ACTUAL: {self.emocion} Adapta todas tus respuestas a este estado emocional de manera sutil pero perceptible."

        return prompt

    async def preguntar(self, mensaje: str) -> str:
        if self.configuracion.historial:
            historial_limitado = (
                self.historial[-AJUSTES_CONTEXTO["max_historial"] :]
                if len(self.historial) > AJUSTES_CONTEXTO["max_historial"]
                else self.historial
            )

            r = await self._agente.run(mensaje, message_history=historial_limitado)
            self.historial.extend(r.new_messages())
        else:
            r = await self._agente.run(mensaje)

        return r.output

    def actualizar_emocion(self, nueva_emocion: str) -> None:
        """Actualiza la emoción y recrea el agente"""
        self.emocion = nueva_emocion
        self._agente = self._crear_agente()
