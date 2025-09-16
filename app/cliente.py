import os

import httpx
from dotenv import load_dotenv
from pydantic import TypeAdapter
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from .configuracion import CONFIG_API, PROMPT_PERSONALIDAD
from .herramientas import HERRAMIENTAS

load_dotenv()
OPEN_ROUTER_TOKEN = os.getenv("OPEN_ROUTER_TOKEN")

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
        OPEN_ROUTER_TOKEN
            Token de API empleado por `OpenRouterProvider`.

    FILES
        app/configuracion.py
            Debe exponer `CONFIG_API` y `PROMPT_PERSONALIDAD`.

    SEE ALSO
        `pydantic_ai.Agent`, `pydantic_ai.models.openai.OpenAIChatModel`,
        `pydantic_ai.providers.openrouter.OpenRouterProvider`.
    """

    def __init__(self, usuario: str, emocion: str) -> None:
        """Inicializa la instancia del cliente.

        PARAMETERS
            usuario
                Identificador del usuario final propagado en cabeceras HTTP para
                trazabilidad y control de uso.

        RETURN VALUES
            None

        ERRORS
            No lanza errores propios, pero podrían propagarse errores durante la
            creación del agente si la configuración o el entorno son inválidos.
        """
        self.usuario = usuario
        self.emocion = emocion
        self.historial: list[ModelMessage] = []
        self.agente = self._crear_agente()

    def _crear_agente(self) -> Agent:
        """Crea y configura el `Agent` subyacente.

        DESCRIPTION
            Construye un `httpx.AsyncClient` con cabeceras de identificación, inicializa
            el modelo `OpenAIChatModel` con `OpenRouterProvider` y aplica los ajustes de
            generación especificados en `CONFIG_API`.

        RETURN VALUES
            Agent
                Instancia lista para ejecutar consultas sincrónicas o asíncronas.

        ERRORS
            Puede propagar errores de red (`httpx`) o de autenticación cuando
            `OPEN_ROUTER_TOKEN` no está presente o es inválido.
        """
        http_client = httpx.AsyncClient(
            headers={
                "HTTP-Referer": CONFIG_API["referente"],
                "X-Title": CONFIG_API["titulo"],
                "user": self.usuario,
            }
        )

        model = OpenAIChatModel(
            CONFIG_API["modelo"],
            provider=OpenRouterProvider(
                api_key=OPEN_ROUTER_TOKEN, http_client=http_client
            ),
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
            system_prompt=(
                PROMPT_PERSONALIDAD
                + f"\n A lunita le ocurrio esto antes de las sesión actual, por lo que adapta su respuestas a sus emociones actuales en su respuesta: {str(self.emocion)}"
            ),
        )

    def preguntar(self, mensaje: str) -> str:
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
        r = self.agente.run_sync(mensaje, message_history=self.historial or None)

        self.historial.extend(r.new_messages())

        return r.output

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

