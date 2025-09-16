import os

import httpx
from dotenv import load_dotenv
from pydantic import TypeAdapter
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from .config import API_CONFIG, PERSONALITY_PROMPT
from .Tools import TOOLS

load_dotenv()
OPEN_ROUTER_TOKEN = os.getenv("OPEN_ROUTER_TOKEN")

MessagesTA = TypeAdapter(list[ModelMessage])


class Client:
    """
    NAME
        Client - Cliente de alto nivel para interactuar con el agente pydantic-ai vía OpenRouter.

    SYNOPSIS
        - c = Client(user)
        - c.ask(message) -> str
        - c.dump_json() -> bytes
        - c.load_json(b) -> None

    DESCRIPTION
        Gestiona la identidad del usuario, el historial de mensajes y la creación de un
        `Agent` configurado con OpenRouter. Expone métodos para consultar al modelo y
        serializar/deserializar el historial de conversación.

    ENVIRONMENT
        OPEN_ROUTER_TOKEN
            Token de API empleado por `OpenRouterProvider`.

    FILES
        app/config.py
            Debe exponer `API_CONFIG` y `PERSONALITY_PROMPT`.

    SEE ALSO
        `pydantic_ai.Agent`, `pydantic_ai.models.openai.OpenAIChatModel`,
        `pydantic_ai.providers.openrouter.OpenRouterProvider`.
    """

    def __init__(self, user: str, mood: str) -> None:
        """Inicializa la instancia del cliente.

        PARAMETERS
            user
                Identificador del usuario final propagado en cabeceras HTTP para
                trazabilidad y control de uso.

        RETURN VALUES
            None

        ERRORS
            No lanza errores propios, pero podrían propagarse errores durante la
            creación del agente si la configuración o el entorno son inválidos.
        """
        self.user = user
        self.mood = mood
        self.history: list[ModelMessage] = []
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """Crea y configura el `Agent` subyacente.

        DESCRIPTION
            Construye un `httpx.AsyncClient` con cabeceras de identificación, inicializa
            el modelo `OpenAIChatModel` con `OpenRouterProvider` y aplica los ajustes de
            generación especificados en `API_CONFIG`.

        RETURN VALUES
            Agent
                Instancia lista para ejecutar consultas sincrónicas o asíncronas.

        ERRORS
            Puede propagar errores de red (`httpx`) o de autenticación cuando
            `OPEN_ROUTER_TOKEN` no está presente o es inválido.
        """
        http_client = httpx.AsyncClient(
            headers={
                "HTTP-Referer": API_CONFIG["referer"],
                "X-Title": API_CONFIG["title"],
                "user": self.user,
            }
        )

        model = OpenAIChatModel(
            API_CONFIG["model"],
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
            tools=TOOLS,
            system_prompt=(
                PERSONALITY_PROMPT
                + f"\n A lunita le ocurrio esto antes de las sesión actual, por lo que adapta su respuestas a sus emociones actuales en su respuesta: {str(self.mood)}"
            ),
        )

    def ask(self, message: str) -> str:
        """Envía una consulta al agente y devuelve la respuesta de texto.

        PARAMETERS
            message
                Mensaje del usuario a enviar al modelo. Si existe historial, se reenvía
                para mantener el contexto conversacional.

        RETURN VALUES
            str
                Salida textual generada por el modelo.

        SIDE EFFECTS
            Actualiza `self.history` con los nuevos mensajes producidos por el agente.

        ERRORS
            Puede propagar errores del proveedor o de red durante la ejecución.
        """
        r = self.agent.run_sync(message, message_history=self.history or None)

        self.history.extend(r.new_messages())

        return r.output

    def dump_json(self) -> bytes:
        """Serializa el historial de conversación a JSON (bytes).

        RETURN VALUES
            bytes
                Representación JSON (UTF-8) del historial actual.
        """
        return MessagesTA.dump_json(self.history)

    def load_json(self, b: bytes) -> None:
        """Restaura el historial de conversación desde una carga JSON.

        PARAMETERS
            b
                Bytes en formato JSON previamente generados por `dump_json()`.

        RETURN VALUES
            None

        ERRORS
            Puede propagar errores de validación si el JSON no es compatible con el
            esquema de `pydantic_ai.messages.ModelMessage`.
        """
        self.history = MessagesTA.validate_json(b)
