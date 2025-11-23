import functools
import logging
import random

from sentiment_analysis_spanish import sentiment_analysis

from .utilidades import CargadorDatos

logger = logging.getLogger(__name__)


class MotorEmocional(CargadorDatos):
    def __init__(self, ruta: str) -> None:
        super().__init__(ruta=ruta)

        self.emocion_actual: int = random.randint(0, len(self._cargar_emociones()) - 1)

        try:
            self.analizador = sentiment_analysis.SentimentAnalysisSpanish()
            logger.info("🔮 Cerebro emocional de Lunita activado correctamente")
        except Exception as e:
            logger.error(f"No se pudo cargar el analizador de sentimientos: {e}")
            self.analizador = None

    def analizar_vibe_usuario(self, mensaje: str) -> bool:
        """
        Analiza el sentimiento del usuario y cambia la emoción de Lunita si es intenso.
        Retorna True si hubo un cambio forzado de emoción.
        """
        if not self.analizador or not mensaje.strip():
            return False

        puntaje = self.analizador.sentiment(mensaje)
        logger.debug(f"Vibe usuario: {puntaje:.3f}")

        # Umbrales más suaves y configurables
        if puntaje > 0.75:
            return self._cambiar_por_valencia(min_valencia=0.6)
        elif puntaje < 0.25:
            return self._cambiar_por_valencia(max_valencia=-0.5)

        return False

    def _cambiar_por_valencia(self, min_valencia=None, max_valencia=None) -> bool:
        candidatos = []
        data = self._cargar_emociones()

        for i, estado in enumerate(data):
            val = estado.get("valencia", 0)
            if min_valencia and val < min_valencia:
                continue
            if max_valencia and val > max_valencia:
                continue
            candidatos.append(i)

        if candidatos:
            self.emocion_actual = random.choice(candidatos)

            logger.info(
                f"Emoción forzada por valencia → {data[self.emocion_actual]['nombre']}"
            )
            return True
        return False

    @functools.lru_cache()
    def _cargar_emociones(self):
        cargador_datos = CargadorDatos("data/emociones.json")
        return cargador_datos.cargar_datos()

    def _buscar_y_establecer(self, keywords: list[str]) -> bool:
        """Busca un estado que contenga alguna de las emociones dadas"""
        emociones_data = self.cargar_datos()
        candidatos = []

        for i, estado in enumerate(emociones_data):
            # Verificamos si alguna emoción del estado coincide con las keywords
            if any(k in estado["emociones"] for k in keywords):
                candidatos.append(i)

        if candidatos:
            self.emocion_actual = random.choice(candidatos)
            nuevo_estado = self.obtener_estado_actual()
            logger.info(
                f"Emoción cambiada por reacción al usuario: {nuevo_estado['emociones']}"
            )
            return True
        return False

    def obtener_estado_actual(self):
        return self._cargar_emociones()[self.emocion_actual]

    def obtener_estado_actual_prompt(self) -> str:
        estado = self.obtener_estado_actual()
        emociones_str = ", ".join(estado["emociones"])
        return f"Emociones actuales: {emociones_str}"

    def obtener_nueva_emocion_al_azar(self):
        """Selecciona y devuelve una nueva emoción aleatoria."""
        emociones = self._cargar_emociones()
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
