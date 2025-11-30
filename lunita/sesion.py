from datetime import datetime
from typing import Optional, TypedDict

from .cliente import Cliente
from .configuracion import ConfigurarEstrellas
from .emocional.motor import MotorEmocional
from .memoria import MemoriaDia


class RespuestaSesion(TypedDict):
    texto: str
    modelo: str
    fecha: datetime


class ConsultasSesion(TypedDict):
    rol: str
    contenido: str
    instrucciones_internas: Optional[str]


class Sesion:
    """Gestiona la sesión de interacción con la IA, incluyendo el estado emocional y el historial de consultas.

    Esta clase encapsula la lógica para manejar la conversación con la IA, incluyendo la gestión del estado emocional
    a través del motor emocional, la memoria diaria y la configuración del cliente.

    Atributes
        configuracion: ConfigurarEstrellas
            Instancia de configuración para la sesión.
    """

    def __init__(self):
        self.configuracion = ConfigurarEstrellas.get_instance()
        self._consultas: list[ConsultasSesion] = []
        # Se ve feo pero es necesario para inicializar la emoción correcta jaja
        if self.configuracion.configuracion_vidente.vidente == "lunita":
            self._recuerdo = MemoriaDia("data/recuerdos_lunita.json")
        elif self.configuracion.configuracion_vidente.vidente == "estrella":
            self._recuerdo = MemoriaDia("data/recuerdos_estrella.json")

        self._emociones = MotorEmocional()

        self._cliente = Cliente(
            emocion=self._recuerdo.obtener_para_prompt(),
        )

    async def predecir(self, pregunta: str) -> RespuestaSesion:
        """Realiza una predicción basada en la pregunta del usuario

        Realiza una consulta al cliente de IA, actualizando el estado emocional según la "vibe" del usuario
        y el recuerdo diario.

        Args:
            pregunta: La pregunta o mensaje del usuario.

        Returns:
            Un diccionario que contiene la respuesta de la IA, el modelo utilizado y la fecha de la respuesta.
        """

        resultado_motor = self._emociones.procesar_mensaje_usuario(pregunta)
        instrucciones_emocion = "\n".join(resultado_motor["instrucciones_asistente"])

        nueva_instruccion = (
            f"(Tu estado emocional es: {self._emociones.emocion_actual_asistente})\n"
        )

        prompt_emociones = f"{self._recuerdo.obtener_recuerdo_completo()}\nEMOCIONES ACTUALES (Ajusta tus respuestas a esta emociones a tus respuestas): {instrucciones_emocion}"
        self._cliente.actualizar_emocion(prompt_emociones)

        return {
            "texto": await self._cliente.preguntar(nueva_instruccion + pregunta),
            "modelo": self.configuracion.modelo,
            "fecha": datetime.now(),
        }

    def cambiar_humor(self) -> str:
        """
        Cambia la emoción actual de la vidente. Todos podemos cambiar de humor incluso Lunita.

        Returns:
            La nueva emoción actual después del cambio.
        """
        return self._emociones.cambiar_emocion_manual()

    @property
    def consultas(self):
        """Obtiene el historial de consultas realizadas.

        Returns:
            Lista de consultas realizadas en la sesión.
        """
        return self._consultas

    @consultas.setter
    def consultas(self, valor):
        """Establece un historial previo de consultas.

        Args:
            valor: Lista de consultas para establecer como historial.
        """
        self._consultas = valor
