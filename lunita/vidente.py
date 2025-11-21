from typing import Literal


class ConfigurarVidente:
    """
    Clase para configurar la vidente a utilizar.
    """

    def __init__(self, vidente: Literal["lunita", "estrella"]) -> None:
        if vidente not in ["lunita", "estrella"]:
            raise ValueError("Vidente no reconocido. Usa 'lunita' o 'estrella'.")

        self.vidente = vidente

    def obtener_prompt(self) -> str:
        """
        Obtiene el prompt correspondiente a la vidente seleccionada.

        Returns:
            str: El prompt de la vidente.
        """
        if self.vidente == "lunita":
            from .constantes import PROMPT_LUNITA

            return PROMPT_LUNITA
        elif self.vidente == "estrella":
            from .constantes import PROMPT_ESTRELLA

            return PROMPT_ESTRELLA
        else:
            raise ValueError("Vidente no reconocido. Usa 'lunita' o 'estrella'.")

    def obtener_mensajes_error(self) -> dict[str, str]:
        """
        Obtiene los mensajes de error correspondientes a la vidente seleccionada.

        Returns:
            dict[str, str]: Los mensajes de error de la vidente.
        """
        if self.vidente == "lunita":
            from .constantes import MENSAJES_ERROR_LUNITA

            return MENSAJES_ERROR_LUNITA
        elif self.vidente == "estrella":
            from .constantes import MENSAJES_ERROR_ESTRELLA

            return MENSAJES_ERROR_ESTRELLA
        else:
            raise ValueError("Vidente no reconocido. Usa 'lunita' o 'estrella'.")
