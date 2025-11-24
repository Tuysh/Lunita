import random

from pysentimiento import create_analyzer

from .utilidades import CargadorDatos


class MotorEmocional(CargadorDatos):
    """Motor para gestionar las emociones de Lunita

    Clase que maneja el estado emocional de Lunita, permitiendo analizar el sentimiento
    de los mensajes del usuario y ajustar las emociones en consecuencia.

    Attributes:
        emocion_actual (int): Índice del estado emocional actual.
    """

    def __init__(self, ruta: str) -> None:
        super().__init__(ruta=ruta)

        self._emociones = self.cargar_datos()
        self.emocion_actual: int = random.randint(0, len(self._emociones) - 1)

        try:
            self.analizador = create_analyzer(task="sentiment", lang="es")
        except Exception as e:
            raise RuntimeError(
                "No se pudo inicializar el analizador de sentimientos."
            ) from e

    def analizar_vibra_usuario(self, mensaje: str) -> bool:
        if not mensaje.strip():
            return False

        resultado = self.analizador.predict(mensaje)

        if resultado.output == "POS":  # type: ignore
            return self._cambiar_por_valencia(min_valencia=0.6)
        elif resultado.output == "NEG":  # type: ignore
            return self._cambiar_por_valencia(max_valencia=-0.5)

        return False

    def _cambiar_por_valencia(self, min_valencia=None, max_valencia=None) -> bool:
        candidatos = []
        data = self._emociones

        for i, estado in enumerate(data):
            val = estado.get("valencia", 0)
            if min_valencia and val < min_valencia:
                continue
            if max_valencia and val > max_valencia:
                continue
            candidatos.append(i)

        if candidatos:
            self.emocion_actual = random.choice(candidatos)
            return True
        return False

    def obtener_estado_actual(self):
        return self._emociones[self.emocion_actual]

    def obtener_estado_actual_prompt(self) -> str:
        estado = self.obtener_estado_actual()
        emociones_str = ", ".join(estado["emociones"])
        return f"Emociones actuales: {emociones_str}"

    def obtener_nueva_emocion_al_azar(self):
        """Selecciona y devuelve una nueva emoción aleatoria."""
        emociones = self._emociones
        if not emociones:
            return {
                "nombre": "curiosa por los astros",
                "emociones": ["curiosidad", "asombro"],
            }

        nueva_emocion = self.emocion_actual
        intentos = 0
        while nueva_emocion == self.emocion_actual and intentos < 10:
            nueva_emocion = random.randint(0, len(emociones) - 1)
            intentos += 1

        self.emocion_actual = nueva_emocion
        emocion_texto = self.obtener_estado_actual()
        return emocion_texto
