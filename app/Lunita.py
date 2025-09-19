"""
NAME
    Lunita - Módulo principal que define la clase controladora de la IA.

DESCRIPTION
    Este módulo contiene la clase `Lunita`, que actúa como la fachada principal para
    interactuar con el chatbot. Integra la lógica de cliente, el motor emocional y
    la moderación de contenido para procesar las entradas de los usuarios y generar
    respuestas coherentes con la personalidad de la IA.
"""

from typing import Optional

from pydantic_ai.messages import ModelMessage

from . import emocional, guardian
from .cliente import Cliente
from .configuracion import MENSAJES_ERROR


class Lunita:
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
        guardian : guardian.Guardian
            Instancia del guardian para moderar el contenido.
        cliente : Cliente
            Instancia del cliente para comunicarse con el modelo de lenguaje.
    """

    def __init__(
        self,
        usuario: str,
        historial: Optional[list[ModelMessage]] = None,
        instrucciones_adiccionales: Optional[str] = None,
    ) -> None:
        """Inicializa una nueva instancia de Lunita.

        PARAMETERS
            usuario
                El identificador único del usuario final.
            historial
                El historial de mensajes para mantener el contexto conversacional.
        """
        self.emocion = emocional.MotorEmocional("./app/json/emociones.json")
        self.guardian = guardian.Guardian()
        self.cliente = Cliente(
            usuario,
            self.emocion.obtener_emocion(),
            instrucciones_adiccionales,
            historial,
        )

    async def predecir(self, mensaje: str) -> str:
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
            return MENSAJES_ERROR["mensaje_invalido"]

        try:
            return await self.cliente.preguntar(mensaje)
        except Exception:
            return MENSAJES_ERROR["error_api"]

    def cambiar_humor(self) -> None:
        """Cambia el humor de Lunita."""
        self.emocion.obtener_nueva_emocion()
