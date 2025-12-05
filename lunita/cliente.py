from typing import Optional

from pydantic import TypeAdapter
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage

from .configuracion import ConfigurarEstrellas
from .constantes import (
    AJUSTES_CONTEXTO,
    DISPARADORES_VERBOSIDAD,
    PROMPT_ESTRELLA,
    PROMPT_LUNITA,
)
from .herramientas import HERRAMIENTAS

AdaptadorMensajes = TypeAdapter(list[ModelMessage])


class Cliente:
    """Cliente de IA que maneja la interacción con el modelo de lenguaje.

    Cliente encapsula la lógica para interactuar con el modelo de lenguaje, gestionando el estado
    emocional y el historial de mensajes para proporcionar respuestas contextualmente relevantes.

    Atributes:
        configuracion (ConfigurarEstrellas): Instancia de configuración para el cliente.
        emocion (str): La emoción actual del cliente IA.
        historial (list[ModelMessage]):
            Historial de mensajes para mantener el contexto de la conversación.
        _agente (Agent): Instancia del agente de IA que maneja las interacciones.
    """

    def __init__(
        self,
        emocion: str,
        historial: Optional[list[ModelMessage]] = None,
    ):
        self.configuracion = ConfigurarEstrellas.get_instance()
        self.emocion = emocion
        self._historial: list[ModelMessage] = historial or []
        self._agente = self._crear_agente()

    def _crear_agente(self) -> Agent:
        """Crea y devuelve una instancia del agente de IA con la configuración actual.

        Configura el agente utilizando el modelo especificado en la configuración, las herramientas
        disponibles y el prompt del sistema que incluye la emoción actual.

        Returns:
            Agent: Una instancia configurada del agente de IA.
        """
        return Agent(
            model=self.configuracion.configuracion_modelo(),
            tools=HERRAMIENTAS,
            system_prompt=self._construir_prompt_sistema(),
        )

    def _construir_prompt_sistema(self) -> str:
        """Construye el prompt del sistema con la emoción actual

        Metodo privado para construir el prompt del sistema que incorpora la emoción actual
        del cliente IA. Selecciona el prompt base según la configuración del vidente y añade la
        instrucción para adaptar las respuestas a la emoción.

        Returns:
            str: El prompt del sistema adaptado a la emoción actual.
        """
        prompt = (
            PROMPT_LUNITA
            if self.configuracion.configuracion_vidente.vidente == "lunita"
            else PROMPT_ESTRELLA
        )
        prompt += f"\n{self.emocion} Adapta todas tus respuestas a este estado emocional de manera sutil pero perceptible."
        return prompt

    def _calcular_factor_verbosidad(self, mensaje: str) -> str:
        """Calcula el factor de verbosidad basado en el mensaje del usuario.

        Determina la longitud apropiada para la respuesta del agente en función de la cantidad
        de palabras en el mensaje del usuario y la presencia de disparadores de verbosidad.

        Args:
            mensaje (str): El mensaje del usuario.

        Returns:
            str: Instrucción de longitud para la respuesta del agente.
        """
        palabras_usuario = len(mensaje.split())
        quiere_verbosidad = any(
            disparador in mensaje.lower() for disparador in DISPARADORES_VERBOSIDAD
        )

        if palabras_usuario < 6 and not quiere_verbosidad:
            return "LENGTH: Be extremely brief. One or two sentences max. Get straight to the point"
        elif 6 <= palabras_usuario <= 18 and not quiere_verbosidad:
            return "LENGTH: Medium-length response. A small paragraph is enough"
        else:
            return "LENGTH: You may elaborate and ramble a bit, but without writing a whole novel"

    async def preguntar(self, mensaje: str) -> str:
        """Realiza una pregunta al agente de IA y obtiene la respuesta.

        Envía el mensaje del usuario al agente de IA, incluyendo el historial de mensajes
        si está habilitado en la configuración. Calcula el factor de verbosidad para adaptar
        la longitud de la respuesta del agente.

        Args:
            mensaje (str): El mensaje del usuario.

        Returns:
            str: La respuesta del agente de IA.
        """
        largo_verbosidad = self._calcular_factor_verbosidad(mensaje)

        mensaje_con_contexto = f"{mensaje} \n ({largo_verbosidad})"

        if self.configuracion.historial:
            historial_limitado = (
                self._historial[-AJUSTES_CONTEXTO["max_historial"] :]
                if len(self._historial) > AJUSTES_CONTEXTO["max_historial"]
                else self._historial
            )

            r = await self._agente.run(
                mensaje_con_contexto, message_history=historial_limitado
            )
            self._historial.extend(r.new_messages())
        else:
            r = await self._agente.run(mensaje_con_contexto)

        return r.output

    def actualizar_emocion(self, nueva_emocion: str) -> None:
        """Actualiza la emoción y recrea el agente

        Metodo para actualizar la emoción del cliente IA y recrear el agente con el nuevo estado
        emocional.

        Args:
            nueva_emocion (str): La nueva emoción para el cliente IA.
        """
        self.emocion = nueva_emocion
        self._agente = self._crear_agente()
