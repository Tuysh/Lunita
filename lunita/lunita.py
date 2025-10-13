import logging
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic_ai.messages import ModelMessage

from . import emocional, guardian
from .cliente import Cliente
from .configuracion import MENSAJES_ERROR
from .memoria import MemoriaAfectiva

logger = logging.getLogger(__name__)


class Lunita:
    """
    Asistente mágico y creativo con memoria afectiva
    """

    def __init__(
        self,
        token: str,
        usuario: str,
        historial: Optional[list[ModelMessage]] = None,
        instrucciones_adicionales: Optional[str] = None,
    ) -> None:
        self.usuario = usuario
        self.emocion = emocional.MotorEmocional("json/emociones.json")
        self.guardian = guardian.Guardian()
        self.memoria = MemoriaAfectiva(
            token=token, modelo="mistral-tiny-latest", max_recuerdos=50
        )

        self.cliente = Cliente(
            token=token,
            usuario=usuario,
            emocion=self.emocion.obtener_para_prompt(),
            instrucciones_adiccionales=instrucciones_adicionales,
            historial=historial,
        )

    async def predecir(self, mensaje: str) -> str:
        """Genera una respuesta basada en el mensaje del usuario"""
        if not self._validar_entrada(mensaje):
            return f"✨ {MENSAJES_ERROR['mensaje_invalido']} ✨"

        try:
            # Buscar recuerdos relevantes con IA
            recuerdos_relevantes = await self.memoria.buscar_recuerdos_relevantes(
                mensaje,
                limite=2,
                usar_ia=True,
            )

            # Generar contexto desde recuerdos
            contexto_memoria = self.memoria.generar_contexto_para_prompt(
                recuerdos_relevantes
            )

            # Añadir contexto al mensaje si existe
            mensaje_con_contexto = mensaje
            if contexto_memoria:
                mensaje_con_contexto = f"{mensaje}\n\n{contexto_memoria}"

            # Obtener respuesta
            respuesta = await self.cliente.preguntar(mensaje_con_contexto)

            # Analizar y guardar en memoria
            await self.memoria.analizar_y_guardar(
                usuario_msg=mensaje,
                lunita_msg=respuesta,
                emocion_lunita=self.emocion,
            )

            return respuesta

        except Exception as e:
            logger.error(f"Error en predicción: {e}")
            return f"✨ {MENSAJES_ERROR['error_api']} ✨"

    def _validar_entrada(self, mensaje: str) -> bool:
        """Validación de entrada del usuario"""
        if not mensaje or not isinstance(mensaje, str):
            return False

        if len(mensaje.strip()) == 0:
            return False

        return self.guardian.obtener_veredicto(mensaje=mensaje)

    def cambiar_humor(self) -> str:
        """Cambia la emoción actual de Lunita"""
        self.emocion.obtener_nueva_emocion()
        self.cliente.actualizar_emocion(self.emocion.obtener_para_prompt())
        logger.info(f"Cambio emocional a: {self.emocion.obtener_emocion()}")
        return str(self.emocion.obtener_emocion())

    def obtener_estado(self) -> Dict[str, Any]:
        """Obtiene el estado actual de Lunita"""
        return {
            "usuario": self.cliente.usuario,
            "emocion_actual": self.emocion.obtener_emocion(),
            "total_mensajes": len(self.cliente.historial),
            "total_recuerdos": len(self.memoria.recuerdos),
            "timestamp": datetime.now().isoformat(),
        }

    async def obtener_perfil_usuario(self) -> dict:
        """Obtiene un perfil completo del usuario desde la memoria"""
        return self.memoria.obtener_perfil_usuario()

    def exportar_historial(self) -> bytes:
        """Exporta el historial de conversación"""
        return self.cliente.exportar_json()

    def importar_historial(self, datos: bytes) -> None:
        """Importa un historial de conversación"""
        self.cliente.importar_json(datos)

    async def cerrar(self):
        """Cierra recursos de la memoria"""
        await self.memoria.close()
