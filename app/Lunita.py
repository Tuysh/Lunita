"""
NAME
    Lunita - Módulo principal que define la clase controladora de la IA.

DESCRIPTION
    Este módulo contiene la clase `Lunita`, que actúa como la fachada principal para
    interactuar con el chatbot. Integra la lógica de cliente, el motor emocional y
    la moderación de contenido para procesar las entradas de los usuarios y generar
    respuestas coherentes con la personalidad de la IA.
"""

import logging

from . import Emocional, Guardian
from .Client import Client
from .config import ERROR_MESSAGES

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Lunita(Guardian.Guardian):
    """
    NAME
        Lunita - Clase principal que implementa la personalidad de una vidente mágica IA.

    SYNOPSIS
        - l = Lunita(user)
        - l.send_message(message) -> str

    DESCRIPTION
        Esta clase es el punto de entrada para interactuar con Lunita. Hereda de
        `Guardian` para incorporar la moderación de contenido y utiliza una instancia
        de `Client` para comunicarse con el modelo de lenguaje y un `MotorEmocional`
        para gestionar estados internos.

    ATTRIBUTES
        user : str
            Identificador del usuario que interactúa con esta instancia.
        emocion : Emocional.MotorEmocional
            Instancia del motor emocional para gestionar el "humor" de Lunita.
        client : Client
            Cliente para interactuar con la API del modelo de lenguaje.
    """

    def __init__(self, user: str) -> None:
        """Inicializa una nueva instancia de Lunita.

        PARAMETERS
            user
                El identificador único del usuario final.
        """
        super().__init__()
        self.user = user
        self.emocion = Emocional.MotorEmocional("./app/json/emociones.json")
        self.client = Client(user=user)

    def send_message(self, message: str) -> str:
        """Procesa un mensaje del usuario y devuelve la respuesta de Lunita.

        DESCRIPTION
            Este método es el principal punto de interacción. Primero, valida que el
            mensaje no esté vacío. Luego, intenta enviar el mensaje al cliente de la IA
            y devuelve la respuesta. Gestiona las excepciones de la API y devuelve
            mensajes de error predefinidos si es necesario.

        PARAMETERS
            message
                El mensaje de texto enviado por el usuario.

        RETURN VALUES
            str
                La respuesta generada por Lunita o un mensaje de error si la entrada
                es inválida o si ocurre un problema con la API.

        ERRORS
            Si la llamada a `self.client.ask(message)` falla, se registra un error
            y se devuelve un mensaje genérico de error de API.
        """
        if not message or not isinstance(message, str):
            return ERROR_MESSAGES["invalid_message"]

        # La moderación de contenido está actualmente desactivada.
        # if not self.getVeredict(message=message):
        #     return ERROR_MESSAGES['invalid_message']

        try:
            return self.client.ask(message)
        except Exception as e:
            logger.error(f"Error al llamar a la API: {str(e)}")
            return ERROR_MESSAGES["api_error"]