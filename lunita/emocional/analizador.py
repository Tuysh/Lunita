from typing import Dict, List

from pysentimiento import create_analyzer

from ..utilidades import CargadorDatos


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

            self._emociones: Dict[str, List[str]] = self.cargar_datos()
            self.emocion_actual_usuario: str = "joy"
            self.instrucciones_actuales: List[str] = []

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
        """Analiza las emociones del usuario y ajusta la emoción actual.

        En esta función se analiza el mensaje del usuario para detectar emociones específicas
        (como alegría, tristeza, miedo, etc.) y se ajusta la emoción actual del asistente en
        consecuencia. Se le añade una cadena de instrucciones basada en las emociones detectadas.

        Args:
            mensaje (str): El mensaje del usuario a analizar.
        Returns:
            str: La emoción detectada en el mensaje del usuario.
        """
        resultado = self._analizador_emocional.predict(mensaje)
        emocion_detectada = resultado.output  # type: ignore

        if emocion_detectada in self._emociones:
            self.emocion_actual_usuario: str = resultado.output  # type: ignore
            self.instrucciones_actuales = self._emociones[self.emocion_actual_usuario]
        else:
            pass

    def obtener_estado_actual_prompt(self) -> str:
        """Obtiene una representación en cadena del estado emocional actual.

        Simplemente devuelve una cadena con todas las emociones actuales para ser usada en algun
        prompt.

        Returns:
            str: La cadena de texto que representa el estado emocional actual.
        """
        return f"(Sigue las siguientes instrucciones: {self.instrucciones_actuales})"
