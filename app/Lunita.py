from typing import List, Dict, Any, Optional
import logging
from . import Context, Emocional, OpenAI, Guardian
from .config import PERSONALITY_PROMPT, API_CONFIG, CONTEXT_SETTINGS, ERROR_MESSAGES

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Lunita(Guardian.Guardian):
    """
    Clase principal que implementa la personalidad de Lunita, una vidente mágica IA.

    Attributes:
        context: Manejador del contexto de la conversación.
        emocion: Motor de análisis emocional.
    """

    def __init__(self) -> None:
        """Inicializa una nueva instancia de Lunita."""
        self.emocion = Emocional.MotorEmocional("./app/json/emociones.json")
        self.context = Context.CreadorContexto(
            PERSONALITY_PROMPT
            + f"\n A lunita le ocurrio esto antes de las sesión actual, por lo que adapta su respuestas a sus emociones actuales en su respuesta: {str(self.emocion.getMood())}",
            CONTEXT_SETTINGS["max_history"],
        )

    def _prepare_messages(self, message: str) -> List[Dict[str, str]]:
        """
        Prepara los mensajes para la API de OpenAI.

        Args:
            message: Mensaje del usuario.

        Returns:
            Lista de mensajes formateados para la API.
        """
        return [*self.context.getHistory(), {"role": "user", "content": message}]

    def _get_api_response(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """
        Obtiene la respuesta de la API de OpenAI.

        Args:
            messages: Lista de mensajes para enviar a la API.

        Returns:
            La respuesta de la API o None si hay un error.
        """
        try:
            completion = OpenAI.clientOpenRouter.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": API_CONFIG["referer"],
                    "X-Title": API_CONFIG["title"],
                },
                model=API_CONFIG["model"],
                temperature=1.5,
                messages=messages,
            )
            return completion.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"Error al llamar a la API: {str(e)}")
            return None

    def send_message(self, message: str) -> str:
        """
        Envía un mensaje a Lunita y devuelve su respuesta.

        Args:
            message: Mensaje del usuario.

        Returns:
            Respuesta de Lunita o mensaje de error.
        """
        if not message or not isinstance(message, str):
            return ERROR_MESSAGES["invalid_message"]

        # if not self.getVeredict(message=message):
        #     return ERROR_MESSAGES['invalid_message']

        messages = self._prepare_messages(message)
        reply = self._get_api_response(messages)

        if reply is None:
            return ERROR_MESSAGES["api_error"]

        self.context.addResponses(user=message, assistant=reply)
        return reply
