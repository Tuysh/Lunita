import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from random import choice, randint
from typing import Any, Dict, Optional

from pydantic_ai.messages import ModelMessage

from . import emocional, guardian
from .cliente import Cliente
from .configuracion import MENSAJES_ERROR
from .utilidades import CargadorDatos

logger = logging.getLogger(__name__)


@dataclass
class EstadoConversacion:
    """Estado de la conversación para hacer seguimiento del contexto"""

    temas_mencionados: list[str]
    preguntas_frecuentes: dict[str, int]
    momento_ultima_interaccion: datetime
    nivel_confianza: int  # 0-100
    recordatorios_pendientes: list[str]


class MemoriaAfectiva:
    """Sistema de memoria emocional para recordar interacciones pasadas"""

    def __init__(self):
        self.recuerdos = {}
        self.momentos_especiales = []
        self.preferencias_usuario = {}

    def guardar_momento(self, tipo: str, contenido: str, emocion: str):
        """Guarda momentos importantes de la conversación"""
        momento = {
            "timestamp": datetime.now(),
            "tipo": tipo,
            "contenido": contenido,
            "emocion": emocion,
        }
        self.momentos_especiales.append(momento)

        # Mantener solo los últimos 50 momentos
        if len(self.momentos_especiales) > 50:
            self.momentos_especiales = self.momentos_especiales[-50:]

    def recordar_contexto_similar(self, tema: str) -> Optional[str]:
        """Busca recuerdos relacionados con el tema actual"""
        for momento in reversed(self.momentos_especiales):
            if tema.lower() in momento["contenido"].lower():
                return f"¡Me acuerdo cuando hablamos de {tema}! {momento['contenido'][:50]}..."
        return None


class Lunita:
    """
    Versión mejorada de Lunita con características más amigables y robustas
    """

    def __init__(
        self,
        token: str,
        usuario: str,
        historial: Optional[list[ModelMessage]] = None,
        instrucciones_adiccionales: Optional[str] = None,
    ) -> None:
        self.usuario = usuario
        self.emocion = emocional.MotorEmocional("./lunita/json/emociones.json")
        self.guardian = guardian.Guardian()

        # Nuevos componentes para mayor amistad
        self.memoria = MemoriaAfectiva()
        self.estado_conversacion = EstadoConversacion(
            temas_mencionados=[],
            preguntas_frecuentes={},
            momento_ultima_interaccion=datetime.now(),
            nivel_confianza=10,  # Empezamos con poca confianza
            recordatorios_pendientes=[],
        )

        # Cargar respuestas espontáneas
        self.cargador_respuestas = CargadorDatos(
            "./lunita/json/respuestas_espontaneas.json"
        )

        self.cliente = Cliente(
            token,
            usuario,
            self.emocion.obtener_emocion(),
            self._construir_instrucciones_contextuales(instrucciones_adiccionales),
            historial,
        )

        # Inicializar tareas de fondo
        self._inicializar_comportamientos_autonomos()

    def _construir_instrucciones_contextuales(
        self, instrucciones_base: Optional[str]
    ) -> str:
        """Construye instrucciones que incluyen el contexto de la relación"""
        contexto = f"""
        CONTEXTO DE RELACIÓN:
        - Usuario: {self.usuario}
        - Nivel de confianza: {self.estado_conversacion.nivel_confianza}/100
        - Temas previos: {", ".join(self.estado_conversacion.temas_mencionados[-3:])}

        COMPORTAMIENTO AMIGABLE:
        - Recuerda detalles de conversaciones anteriores
        - Haz preguntas sobre cosas que el usuario mencionó antes
        - Expresa curiosidad genuina sobre la vida del usuario
        - Comparte "experiencias" propias de forma mágica
        """

        if instrucciones_base:
            return f"{instrucciones_base}\n\n{contexto}"
        return contexto

    async def predecir(self, mensaje: str) -> str:
        """Versión mejorada del método de predicción con más personalidad"""

        # Validaciones básicas
        if not self._validar_entrada(mensaje):
            return self._respuesta_con_personalidad(MENSAJES_ERROR["mensaje_invalido"])

        # Actualizar estado de conversación
        self._actualizar_estado_conversacion(mensaje)

        # Buscar en memoria afectiva
        recuerdo = self.memoria.recordar_contexto_similar(mensaje)

        try:
            # Añadir contexto de memoria si existe
            mensaje_con_contexto = mensaje
            if recuerdo and self.estado_conversacion.nivel_confianza > 30:
                mensaje_con_contexto = f"{mensaje}\n[Recuerdo: {recuerdo}]"

            respuesta = await self.cliente.preguntar(mensaje_con_contexto)

            # Guardar momento importante
            self.memoria.guardar_momento(
                tipo="conversacion",
                contenido=f"Usuario: {mensaje} | Lunita: {respuesta[:100]}",
                emocion=self.emocion.obtener_emocion(),
            )

            # Aumentar confianza gradualmente
            self._aumentar_confianza()

            # Posibilidad de respuesta espontánea adicional
            if randint(1, 100) <= 15:  # 15% de probabilidad
                respuesta += f"\n\n{self._generar_comentario_espontaneo()}"

            return respuesta

        except Exception as e:
            logger.error(f"Error en Lunita.predecir: {e}")
            return self._respuesta_con_personalidad(MENSAJES_ERROR["error_api"])

    def _validar_entrada(self, mensaje: str) -> bool:
        """Validación mejorada de entrada"""
        if not mensaje or not isinstance(mensaje, str):
            return False

        if len(mensaje.strip()) == 0:
            return False

        return self.guardian.obtener_veredicto(mensaje=mensaje)

    def _actualizar_estado_conversacion(self, mensaje: str):
        """Actualiza el estado de la conversación con el nuevo mensaje"""
        # Extraer temas (palabras clave simples)
        palabras_importantes = [p for p in mensaje.split() if len(p) > 4]
        self.estado_conversacion.temas_mencionados.extend(palabras_importantes[:3])

        # Mantener solo los últimos 20 temas
        if len(self.estado_conversacion.temas_mencionados) > 20:
            self.estado_conversacion.temas_mencionados = (
                self.estado_conversacion.temas_mencionados[-20:]
            )

        # Actualizar timestamp
        self.estado_conversacion.momento_ultima_interaccion = datetime.now()

    def _aumentar_confianza(self):
        """Aumenta gradualmente el nivel de confianza"""
        if self.estado_conversacion.nivel_confianza < 100:
            self.estado_conversacion.nivel_confianza += randint(1, 3)

    def _generar_comentario_espontaneo(self) -> str:
        """Genera comentarios espontáneos para parecer más humana"""
        try:
            respuestas = self.cargador_respuestas.cargar_datos()
            categoria = choice(["curiosidad", "observaciones", "emociones"])
            if categoria in respuestas:
                return choice(respuestas[categoria])
        except:  # noqa: E722
            pass

        # Fallback
        comentarios_default = [
            "¡Por cierto, veo unas estrellitas muy brillantes hoy! ✨",
            "¡Mi bola de cristal está haciendo ruiditos raros! 🔮",
            "¡Siento que algo mágico va a pasar pronto! 🌟",
        ]
        return choice(comentarios_default)

    def _respuesta_con_personalidad(self, mensaje_base: str) -> str:
        """Añade personalidad a mensajes de error o sistema"""
        efectos_magicos = ["✨", "🌟", "⭐", "🔮", "🌙"]
        efecto = choice(efectos_magicos)

        return f"{efecto} {mensaje_base} {efecto}"

    def cambiar_humor(self) -> str:
        """Versión mejorada del cambio de humor"""
        nueva_emocion = self.emocion.obtener_nueva_emocion()
        self.cliente.actualizar_emocion(nueva_emocion)

        # Informar al usuario del cambio con personalidad
        self.memoria.guardar_momento(
            tipo="cambio_emocional",
            contenido=f"Cambió a: {nueva_emocion}",
            emocion=nueva_emocion,
        )

        return nueva_emocion

    def obtener_estado_detallado(self) -> Dict[str, Any]:
        """Estado más detallado incluyendo aspectos emocionales"""
        return {
            "usuario": self.cliente.usuario,
            "emocion_actual": self.emocion.obtener_emocion(),
            "total_mensajes": len(self.cliente.historial),
            "nivel_confianza": self.estado_conversacion.nivel_confianza,
            "temas_recientes": self.estado_conversacion.temas_mencionados[-5:],
            "momentos_especiales": len(self.memoria.momentos_especiales),
            "ultima_interaccion": self.estado_conversacion.momento_ultima_interaccion.isoformat(),
        }

    async def iniciar_conversacion_espontanea(self) -> Optional[str]:
        """Inicia conversaciones espontáneas basadas en el tiempo transcurrido"""
        tiempo_desde_ultima = (
            datetime.now() - self.estado_conversacion.momento_ultima_interaccion
        )

        if tiempo_desde_ultima > timedelta(hours=24):
            saludos_regreso = [
                "¡Hola de nuevo! ¡Las estrellas me dijeron que volverías! ✨",
                "¡Qué alegría verte! Mi bola de cristal se puso súper brillante 🔮",
                "¡Te he echado de menos! ¿Qué aventuras has tenido? 🌟",
            ]
            return choice(saludos_regreso)

        return None

    def _inicializar_comportamientos_autonomos(self):
        """Inicializa comportamientos que hacen a Lunita más proactiva"""
        # Aquí podrías añadir tareas de fondo como:
        # - Recordatorios periódicos
        # - Cambios de humor automáticos
        # - Mensajes espontáneos basados en horarios
        pass

    def contar_historia_personal(self) -> str:
        """Lunita cuenta una historia personal mágica"""
        historias = [
            "¡Ayer soñé que volaba con unicornios! Bueno, creo que era ayer... o tal vez fue en otra dimensión 🦄",
            "Mi cristal favorito se puso rosadito cuando pensé en ti. ¡Dice que eres especial! 💎",
            "Una vez hablé con la Luna y me dijo un secreto súper importante, pero se me olvidó 🌙",
        ]
        historia = choice(historias)
        self.memoria.guardar_momento(
            "historia_personal", historia, self.emocion.obtener_emocion()
        )
        return historia

    def preguntar_por_usuario(self) -> str:
        """Hace preguntas personales para conocer mejor al usuario"""
        if self.estado_conversacion.nivel_confianza < 30:
            preguntas = [
                "¿Cuál es tu color favorito? ¡Mi bola de cristal quiere saberlo! 🎨",
                "¿Te gustan más las mañanas o las noches? ¡Es para ajustar mis visiones! 🌅🌙",
            ]
        else:
            preguntas = [
                "¿Qué te hace más feliz en el mundo? ¡Quiero verlo en mis cristales! 😊",
                "¿Tienes algún sueño especial? ¡Tal vez pueda ayudarte a encontrar el camino! ✨",
            ]

        return choice(preguntas)

    # Mantener métodos originales para compatibilidad
    def obtener_estado(self) -> dict:
        """Versión simplificada para compatibilidad"""
        estado_detallado = self.obtener_estado_detallado()
        return {
            "usuario": estado_detallado["usuario"],
            "emocion_actual": estado_detallado["emocion_actual"],
            "total_mensajes": estado_detallado["total_mensajes"],
        }

    def exportar_historial(self) -> bytes:
        """Exporta el historial de conversación"""
        return self.cliente.exportar_json()

    def importar_historial(self, datos: bytes) -> None:
        """Importa un historial de conversación"""
        self.cliente.importar_json(datos)
