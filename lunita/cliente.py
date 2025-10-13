from typing import Optional

import httpx
from pydantic import TypeAdapter
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider

from .configuracion import AJUSTES_CONTEXTO, CONFIG_API, PROMPT_PERSONALIDAD
from .herramientas import HERRAMIENTAS

AdaptadorMensajes = TypeAdapter(list[ModelMessage])


class Cliente:
    """
    NAME
        Cliente - Cliente de alto nivel para interactuar con el agente pydantic-ai vía OpenRouter.

    SYNOPSIS
        - c = Cliente(usuario)
        - c.preguntar(mensaje) -> str
        - c.exportar_json() -> bytes
        - c.importar_json(b) -> None

    DESCRIPTION
        Gestiona la identidad del usuario, el historial de mensajes y la creación de un
        `Agent` configurado con OpenRouter. Expone métodos para consultar al modelo y
        serializar/deserializar el historial de conversación.

    ENVIRONMENT
        MINISTRAL_TOKEN
            Token de API empleado por `MistralProvider`.

    FILES
        app/configuracion.py
            Debe exponer `CONFIG_API` y `PROMPT_PERSONALIDAD`.

    SEE ALSO
        `pydantic_ai.Agent`, `pydantic_ai.models.mistral.MistralModel`,
        `pydantic_ai.providers.mistral.MistralProvider`.
    """

    def __init__(
        self,
        token: str,
        usuario: str,
        emocion: str,
        instrucciones_adiccionales: Optional[str] = None,
        historial: Optional[list[ModelMessage]] = None,
    ) -> None:
        """Inicializa la instancia del cliente.

        PARAMETERS
            token
                Token de API empleado por `MistralProvider`.
            usuario
                Identificador del usuario final propagado en cabeceras HTTP para
                trazabilidad y control de uso.
            emocion
                El estado emocional actual de Lunita, que se refleja en su respuesta.
            instrucciones_adiccionales
                Instrucciones adicionales para el agente, que pueden ser utilizadas
                para modificar su comportamiento.
            historial
                El historial de mensajes para mantener el contexto conversacional.

        RETURN VALUES
            None

        ERRORS
            No lanza errores propios, pero podrían propagarse errores durante la
            creación del agente si la configuración o el entorno son inválidos.
        """
        self.token = token
        self.usuario = usuario
        self.emocion = emocion
        self.instrucciones_adiccionales = instrucciones_adiccionales
        self.historial: list[ModelMessage] = historial or []
        self.agente = self._crear_agente()

    def _crear_agente(self) -> Agent:
        """Crea y configura el `Agent` subyacente.

        DESCRIPTION
            Construye un `httpx.AsyncClient` con cabeceras de identificación, inicializa
            el modelo `MistralModel` con `MistralProvider` y aplica los ajustes de
            generación especificados en `CONFIG_API`.

        RETURN VALUES
            Agent
                Instancia lista para ejecutar consultas sincrónicas o asíncronas.

        ERRORS
            Puede propagar errores de red (`httpx`) o de autenticación cuando
            `Ministral Token` no está presente o es inválido.
        """
        http_client = httpx.AsyncClient(
            headers={
                "HTTP-Referer": CONFIG_API["referente"],
                "X-Title": CONFIG_API["titulo"],
                "user": self.usuario,
            }
        )

        model = MistralModel(
            model_name=CONFIG_API["modelo"],
            provider=MistralProvider(api_key=self.token, http_client=http_client),
            settings={
                "max_tokens": 500,
                "temperature": 1.5,
                "top_p": 0.9,
                "frequency_penalty": 0.5,
                "presence_penalty": 0.5,
            },
        )

        return Agent(
            model,
            tools=HERRAMIENTAS,
            system_prompt=self._construir_prompt_sistema(),
        )

    def _construir_prompt_sistema(self) -> str:
        """Construye el prompt del sistema con la emoción actual"""
        prompt = PROMPT_PERSONALIDAD
        prompt += f"\n\nESTADO EMOCIONAL ACTUAL: \n{self.emocion}"
        prompt += "\nAdapta todas tus respuestas a este estado emocional de manera sutil pero perceptible."

        if self.instrucciones_adiccionales:
            prompt += (
                f"\n\nINSTRUCCIONES ADICIONALES: {self.instrucciones_adiccionales}"
            )

        return prompt

    async def preguntar(self, mensaje: str) -> str:
        """Envía una consulta al agente y devuelve la respuesta de texto.

        PARAMETERS
            mensaje
                Mensaje del usuario a enviar al modelo. Si existe historial, se reenvía
                para mantener el contexto conversacional.

        RETURN VALUES
            str
                Salida textual generada por el modelo.

        SIDE EFFECTS
            Actualiza `self.historial` con los nuevos mensajes producidos por el agente.

        ERRORS
            Puede propagar errores del proveedor o de red durante la ejecución.
        """
        historial_limitado = (
            self.historial[-AJUSTES_CONTEXTO["max_historial"] :]
            if len(self.historial) > AJUSTES_CONTEXTO["max_historial"]
            else self.historial
        )

        r = await self.agente.run(mensaje, message_history=historial_limitado)

        self.historial.extend(r.new_messages())

        return r.output

    def actualizar_emocion(self, nueva_emocion: str) -> None:
        """Actualiza la emoción y recrea el agente"""
        self.emocion = nueva_emocion
        self.agente = self._crear_agente()

    def exportar_json(self) -> bytes:
        """Serializa el historial de conversación a JSON (bytes).

        RETURN VALUES
            bytes
                Representación JSON (UTF-8) del historial actual.
        """
        return AdaptadorMensajes.dump_json(self.historial)

    def importar_json(self, b: bytes) -> None:
        """Restaura el historial de conversación desde una carga JSON.

        PARAMETERS
            b
                Bytes en formato JSON previamente generados por `exportar_json()`.

        RETURN VALUES
            None

        ERRORS
            Puede propagar errores de validación si el JSON no es compatible con el
            esquema de `pydantic_ai.messages.ModelMessage`.
        """
        self.historial = AdaptadorMensajes.validate_json(b)
