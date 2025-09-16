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

from . import emocional, guardian
from .cliente import Cliente
from .configuracion import MENSAJES_ERROR

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Lunita(guardian.Guardian):
    """
    NAME
        Lunita - Clase principal que implementa la personalidad de una vidente mágica IA.

    SYNOPSIS
        - l = Lunita(usuario)
        - l.enviar_mensaje(mensaje) -> str

    DESCRIPTION
        Esta clase es el punto de entrada para interactuar con Lunita. Hereda de
        `Guardian` para incorporar la moderación de contenido y utiliza una instancia
        de `Cliente` para comunicarse con el modelo de lenguaje y un `MotorEmocional`
        para gestionar estados internos.

    ATTRIBUTES
        usuario : str
            Identificador del usuario que interactúa con esta instancia.
        emocion : emocional.MotorEmocional
            Instancia del motor emocional para gestionar el "humor" de Lunita.
        cliente : Cliente
            Cliente para interactuar con la API del modelo de lenguaje.
    """

    def __init__(self, usuario: str) -> None:
        """Inicializa una nueva instancia de Lunita.

        PARAMETERS
            usuario
                El identificador único del usuario final.
        """
        super().__init__()
        self.usuario = usuario
        self.emocion = emocional.MotorEmocional("./app/json/emociones.json")
        self.cliente = Cliente(usuario=usuario, emocion=self.emocion.obtener_emocion())

    def enviar_mensaje(self, mensaje: str) -> str:
        """Procesa un mensaje del usuario y devuelve la respuesta de Lunita.

        DESCRIPTION
            Este método es el principal punto de interacción. Primero, valida que el
            mensaje no esté vacío. Luego, intenta enviar el mensaje al cliente de la IA
            y devuelve la respuesta. Gestiona las excepciones de la API y devuelve
            mensajes de error predefinidos si es necesario.

        PARAMETERS
            mensaje
                El mensaje de texto enviado por el usuario.

        RETURN VALUES
            str
                La respuesta generada por Lunita o un mensaje de error si la entrada
                es inválida o si ocurre un problema con la API.

        ERRORS
            Si la llamada a `self.cliente.preguntar(mensaje)` falla, se registra un error
            y se devuelve un mensaje genérico de error de API.
        """
        if not mensaje or not isinstance(mensaje, str):
            return MENSAJES_ERROR["mensaje_invalido"]

        if not self.obtener_veredicto(message=mensaje):
            return MENSAJES_ERROR['mensaje_invalido']

        try:
            return self.cliente.preguntar(mensaje)
        except Exception as e:
            logger.error(f"Error al llamar a la API: {str(e)}")
            return MENSAJES_ERROR["error_api"]