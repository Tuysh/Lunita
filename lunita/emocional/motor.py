from random import random
from typing import TypedDict, NotRequired, List

from .analizador import AnalizardorEmocional
from .emocion import AdministradorEmocional


class RespuestaMotorEmocional(TypedDict):
    emocion_asistente: NotRequired[str]
    emocion_usuario: NotRequired[str]
    instrucciones_asistente: List[str]


class MotorEmocional:
    """Motor emocional que gestiona las emociones del asistente IA y del usuario.

    En esta clase se integran el analizador emocional y el administrador emocional para
    gestionar las emociones tanto del asistente IA como del usuario. Proporciona métodos para
    procesar los mensajes del usuario y ajustar las emociones en consecuencia. Ejemplo de uso:
        motor = MotorEmocional()
        respuesta = motor.procesar_mensaje_usuario("Estoy muy feliz hoy")

    Atributes:
        emocion_actual_asistente (str): La emoción actual del asistente IA.
        instrucciones_actuales (List[str]): Las instrucciones actuales para el asistente IA.

    """

    def __init__(self) -> None:
        self._analizador_emocional = AnalizardorEmocional(
            ruta="data/emociones_entrada_lunita.json"
        )
        self._administrador_emocional = AdministradorEmocional(
            ruta="data/emociones_lunita.json"
        )

        self.emocion_actual_asistente: str = (
            self._administrador_emocional.emocion_actual
        )
        self.instrucciones_actuales: List[str] = (
            self._administrador_emocional.instrucciones_actuales
        )

    def procesar_mensaje_usuario(self, mensaje: str) -> RespuestaMotorEmocional:
        """Procesa el mensaje del usuario y ajusta las emociones en consecuencia.

        Analiza el mensaje del usuario para determinar su emoción actual y ajusta la emoción del
        asistente IA en función de la "vibra" del usuario y una probabilidad aleatoria.

        Args:
            mensaje (str): El mensaje del usuario a procesar.
        Returns:
            RespuestaMotorEmocional: Un diccionario que contiene las emociones actuales del
            asistente y del usuario, así como las instrucciones para el asistente.
        """
        emocion_cambiada = self._analizador_emocional.analizar_vibra_usuario(mensaje)

        if not emocion_cambiada and random() < 0.3:
            self.emocion_actual_asistente = (
                self._administrador_emocional.obtener_nueva_emocion_al_azar()
            )
            self.instrucciones_actuales = (
                self._administrador_emocional.instrucciones_actuales
            )

            return {
                "emocion_asistente": self.emocion_actual_asistente,
                "instrucciones_asistente": self.instrucciones_actuales,
            }

        if emocion_cambiada:
            self.instrucciones_actuales = (
                self._analizador_emocional.instrucciones_actuales
            )

        return {
            "emocion_usuario": self._analizador_emocional.emocion_actual_usuario,
            "instrucciones_asistente": self.instrucciones_actuales,
        }

    def cambiar_emocion_manual(self) -> str:
        """Fuerza un cambio de emoción al azar para el asistente.

        Returns:
            str: El nombre de la nueva emoción.
        """
        self.emocion_actual_asistente = (
            self._administrador_emocional.obtener_nueva_emocion_al_azar()
        )
        self.instrucciones_actuales = (
            self._administrador_emocional.instrucciones_actuales
        )
        return self.emocion_actual_asistente
