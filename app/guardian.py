import logging

from spanlp.palabrota import Palabrota

logger = logging.getLogger(__name__)


class Guardian:
    """
    NAME
        Guardian - Clase para la moderación de contenido.

    SYNOPSIS
        - g = Guardian()
        - g.obtener_veredicto(message) -> bool

    DESCRIPTION
        Esta clase se encarga de analizar los mensajes de los usuarios para determinar
        si cumplen con las directrices de contenido. Utiliza un método interno que
        se espera que interactúe con una API de moderación.
    """

    def __init__(self):
        self.palabrota = Palabrota()

    def obtener_veredicto(self, mensaje: str) -> bool:
        """Determina si un mensaje es apropiado según las directrices.

        DESCRIPTION
            Analiza el mensaje utilizando el detector de palabrotas y devuelve
            `True` si el mensaje no contiene palabrotas, lo que indica que es
            apropiado.

        PARAMETERS
            message
                El mensaje del usuario a verificar.

        RETURN VALUES
            bool
                `True` si el mensaje es apropiado, `False` si ha sido marcado como
                inapropiado.
        """
        try:
            if not mensaje or not isinstance(mensaje, str):
                return False

            es_apropiado = not self.palabrota.contains_palabrota(mensaje.strip())

            if not es_apropiado:
                logger.warning("Mensaje inapropiado detectado")

            return es_apropiado

        except Exception as e:
            logger.error(f"Error en Guardian.obtener_veredicto: {e}")
            # En caso de error, ser conservador y rechazar
            return False

    def analizar_contenido(self, mensaje: str) -> dict:
        """Análisis más detallado del contenido (para futuras mejoras)"""
        return {
            "es_apropiado": self.obtener_veredicto(mensaje),
            "longitud": len(mensaje),
            "palabras": len(mensaje.split()) if mensaje else 0,
        }
