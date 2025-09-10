from .Typos import Mensaje
import secrets
from typing import List


class CreadorContexto:
    """
    Creador de contexto para los asistentes de Cualli Labs
    """

    def __init__(self, system_prompt: str, max_length: int) -> None:
        self.system_prompt = system_prompt
        self.seed = secrets.randbelow(100)
        self.max_length = max_length
        self._mensajes: List[Mensaje] = []
        self._mensajes.append({
            "role": "system",
            "content": system_prompt
        })

    def getHistory(self) -> List[Mensaje]:
        """Obtener todos los mensajes."""
        return self._mensajes

    def addResponses(self, user: str, assistant: str) -> None:
        """
        Añadir turno user/assistant al contexto.
        (Guardamos ambos si caben 2 entradas más)
        """
        if len(self._mensajes) + 2 <= self.max_length:
            self._mensajes.append({"role": "user", "content": user})
            self._mensajes.append({"role": "assistant", "content": assistant})

    def summarize(self):
        """Resume la conversación (pendiente)."""
        print("Resumir...")
        pass