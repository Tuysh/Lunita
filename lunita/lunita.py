import logging
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic_ai.messages import ModelMessage

from . import emocional, guardian
from .cliente import Cliente
from .configuracion import MENSAJES_ERROR

logger = logging.getLogger(__name__)


class Lunita:
    """
    Asistente mágico y creativo
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
        self.guardian = guardian.Guardian(token=token)

        self.cliente = Cliente(
            token=token,
            usuario=usuario,
            emocion=self.emocion.obtener_para_prompt(),
            instrucciones_adiccionales=instrucciones_adicionales,
            historial=historial,
        )

    async def predecir(self, mensaje: str) -> str:
        """Genera una respuesta basada en el mensaje del usuario"""
        if not await self._validar_entrada(mensaje):
            return f"✨ {MENSAJES_ERROR['mensaje_invalido']} ✨"

        try:

            # Obtener respuesta
            respuesta = await self.cliente.preguntar(mensaje)

            return respuesta

        except Exception as e:
            logger.error(f"Error en predicción: {e}")
            return f"✨ {MENSAJES_ERROR['error_api']} ✨"

    async def _validar_entrada(self, mensaje: str) -> bool:
        """Validación de entrada del usuario"""
        if not mensaje or not isinstance(mensaje, str):
            return False

        if len(mensaje.strip()) == 0:
            return False

        return await self.guardian.obtener_veredicto(mensaje=mensaje)

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
            "timestamp": datetime.now().isoformat(),
        }

    def exportar_historial(self) -> bytes:
        """Exporta el historial de conversación"""
        return self.cliente.exportar_json()

    def importar_historial(self, datos: bytes) -> None:
        """Importa un historial de conversación"""
        self.cliente.importar_json(datos)

