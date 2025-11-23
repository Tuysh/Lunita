import random
from typing import TypedDict

from .utilidades import CargadorDatos


class Recuerdo(TypedDict):
    situacion: str
    emociones: list[str]


class MemoriaDia(CargadorDatos):
    def __init__(self, ruta):
        super().__init__(ruta)
        self.recuerdos = self.cargar_datos()
        self.recuerdo_actual: Recuerdo = random.choice(self.recuerdos)

    def obtener_recuerdo_completo(self) -> str:
        return f"HOY TE PASO: {self.recuerdo_actual['situacion']}"

    def obtener_contexto_emocional(self) -> str:
        emos = ", ".join(self.recuerdo_actual["emociones"])
        return f"Emociones de fondo por lo de hoy: {emos}"

    def obtener_emociones(self) -> Recuerdo:
        """Obtiene la emoción actual.

        RETURN VALUES
            str
                La cadena de texto que representa la emoción actual.
        """
        return self.cargar_datos()[self.emocion_actual]

    def obtener_para_prompt(self) -> str:
        """Formato limpio para incluir en el system prompt"""
        emociones_str = self.obtener_contexto_emocional()

        return f"{self.obtener_recuerdo_completo()}\nSentimientos: {emociones_str}\n"

    def obtener_nueva_emocion(self) -> Recuerdo:
        """Selecciona y devuelve una nueva emoción aleatoria.

        SIDE EFFECTS
            Modifica el atributo `self.emocion_actual` a un nuevo valor aleatorio.

        RETURN VALUES
            str
                La cadena de texto de la nueva emoción seleccionada.
        """
        emociones = self.cargar_datos()
        if not emociones:
            return {
                "situacion": "curiosa por los astros",
                "emociones": ["curiosidad", "asombro"],
            }

        nueva_emocion = self.emocion_actual
        intentos = 0
        while nueva_emocion == self.emocion_actual and intentos < 10:
            nueva_emocion = random.randint(0, len(emociones) - 1)
            intentos += 1

        self.emocion_actual = nueva_emocion
        emocion_texto = self.obtener_emociones()
        return emocion_texto

    def establecer_emocion_especifica(self, emocion: str) -> bool:
        """Establece una emoción específica si existe en la lista"""
        emociones = self.cargar_datos()
        try:
            indice = emociones.index(emocion)  # type: ignore
            self.emocion_actual = indice
            return True
        except ValueError:
            raise ValueError(f"Emoción {emocion} no encontrada")
