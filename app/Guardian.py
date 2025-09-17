from spanlp.palabrota import Palabrota


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

    def obtener_veredicto(self, message: str) -> bool:
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
        return not self.palabrota.contains_palabrota(message)
