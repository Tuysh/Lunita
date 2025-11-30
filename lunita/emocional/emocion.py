from random import choice
from typing import Dict, List

from ..utilidades import CargadorDatos


class AdministradorEmocional(CargadorDatos):
    """Administrador para gestionar las emociones de Lunita

    Clase que maneja el estado emocional de Lunita, permitiendo obtener y cambiar las emociones. En
    almacena la emocion actual y proporciona métodos para obtener la emocion y instrucciones
    actuales, para que siga esas directrices en sus respuestas.
    """

    def __init__(
        self,
        ruta: str,
    ) -> None:
        super().__init__(ruta=ruta)

        self._emociones: Dict[str, List[str]] = self.cargar_datos()
        self.emocion_actual: str = choice(list(self._emociones.keys()))
        self.instrucciones_actuales: List[str] = self._emociones[self.emocion_actual]

    def obtener_emocion_actual_prompt(self) -> str:
        """Obtiene una representación en cadena del estado emocional actual.

        Simplemente devuelve una cadena con todas las emociones actuales para ser usada en algun
        prompt.

        Returns:
            str: La cadena de texto que representa el estado emocional actual.
        """
        return f"(Emocion actual: {self.emocion_actual}, instrucciones: {self._emociones[self.emocion_actual]})"

    def obtener_nueva_emocion_al_azar(self) -> str:
        """Selecciona y devuelve una nueva emoción aleatoria.

        Selecciona una nueva emoción al azar que sea diferente a la actual con hasta 10 intentos.
        Si no se encuentra una emoción diferente, se mantiene la actual.

        Returns:
            str: La cadena de texto de la nueva emoción seleccionada.
        """

        nueva_emocion = choice(list(self._emociones.keys()))
        intentos = 0

        while nueva_emocion == self.emocion_actual and intentos < 10:
            nueva_emocion = choice(list(self._emociones.keys()))
            intentos += 1

        self.emocion_actual = nueva_emocion
        self.instrucciones_actuales = self._emociones[self.emocion_actual]
        return nueva_emocion
