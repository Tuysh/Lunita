from random import choice
from typing import TypedDict

from pysentimiento import create_analyzer

from ..utilidades import CargadorDatos


class EstadoEmocional(TypedDict):
    situacion: str
    emociones: list[str]
    valencia: float
    intensidad: float


class AnalizardorEmocional(CargadorDatos):
    """Analizador emocional para gestionar las emociones del asistente IA

    En esta clase se maneja el estado emocional del asistente, permitiendo analizar el sentimiento
    de los mensajes del usuario y ajustar las emociones en consecuencia. En general controla las
    emociones en funcion del mensaje de entrada del usuario. Ejemplo de uso:

        analizador = AnalizardorEmocional(lang="es", task="sentiment", ruta="ruta/a/archivo.json")
        analizador.analizar_vibra_usuario("Me siento feliz hoy")

    Raises:
        RuntimeError: Si no se puede inicializar el analizador de sentimientos.

    """

    def __init__(
        self,
        ruta: str,
    ) -> None:
        try:
            super().__init__(ruta=ruta)

            self._analizador_sentimental = create_analyzer(task="sentiment", lang="es")
            self._analizador_emocional = create_analyzer(task="emotion", lang="es")

            self._emociones: list[EstadoEmocional] = self.cargar_datos()
            self.emocion_actual: EstadoEmocional = choice(self._emociones)
            self.instrucciones_actuales: str = ""

        except Exception as e:
            raise RuntimeError(
                "No se pudo inicializar el analizador de sentimientos."
            ) from e

    def analizar_vibra_usuario(self, mensaje: str) -> bool:
        """Analiza el mensaje del usuario y ajusta la emoción en consecuencia.

        Analiza el mensaje del usuario y ajusta la emoción actual según el sentimiento detectado. En
        general, los mensajes positivos aumentan la valencia emocional, mientras que los negativos
        la disminuyen. Ya para elegir un nuevo estado emocional, se selecciona aleatoriamente entre
        los estados que cumplen con el criterio de valencia.

        Args:
            mensaje (str): El mensaje del usuario a analizar.

        Returns:
            bool: True si se cambió la emoción actual, False en caso contrario.
        """
        if not mensaje.strip():
            return False

        resultado = self._analizador_sentimental.predict(mensaje)

        if resultado.output != "NEU":  # type: ignore
            self._analizar_emociones_usuario(mensaje)
            return True

        return False

    def _analizar_emociones_usuario(self, mensaje: str):
        resultado = self._analizador_emocional.predict(mensaje)

        self.emocion_actual = resultado.output  # type: ignore
        self.instrucciones_actuales = ", ".join(self._emociones[self.emocion_actual])  # type: ignore

        return resultado.output  # type: ignore

    def obtener_estado_actual_prompt(self) -> str:
        """Obtiene una representación en cadena del estado emocional actual.

        Simplemente devuelve una cadena con todas las emociones actuales para ser usada en algun
        prompt.

        Returns:
            str: La cadena de texto que representa el estado emocional actual.
        """
        estado = self.emocion_actual
        emociones_str = ", ".join(estado["emociones"])
        return f"Emociones actuales: {emociones_str}"

    def obtener_nueva_emocion_al_azar(self) -> EstadoEmocional:
        """Selecciona y devuelve una nueva emoción aleatoria.

        Selecciona una nueva emoción al azar que sea diferente a la actual con hasta 10 intentos.
        Si no se encuentra una emoción diferente, se mantiene la actual.

        Returns:
            str: La cadena de texto de la nueva emoción seleccionada.
        """

        nueva_emocion = choice(self._emociones)
        intentos = 0

        while nueva_emocion == self.emocion_actual and intentos < 10:
            nueva_emocion = choice(self._emociones)
            intentos += 1

        self.emocion_actual = nueva_emocion
        return nueva_emocion
