import logging

from . import Emocional, Guardian
from .Client import create_agent
from .config import ERROR_MESSAGES

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Lunita(Guardian.Guardian):
    """
    Clase principal que implementa la personalidad de Lunita, una vidente mágica IA.

    Attributes:
        emocion: Motor de análisis emocional.
    """

    def __init__(self, user: str) -> None:
        """Inicializa una nueva instancia de Lunita."""
        self.user = user
        self.emocion = Emocional.MotorEmocional("./app/json/emociones.json")
        self.agent = create_agent(self.user)

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

        try:
            reply = self.agent.run_sync(message)
            return reply
        except Exception as e:
            logger.error(f"Error al llamar a la API: {str(e)}")
            return ERROR_MESSAGES["api_error"]
