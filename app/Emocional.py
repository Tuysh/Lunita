import random
import json


class ObtenerDatos:
    """
    Clase para obtener datos
    """

    def __init__(self, ruta) -> None:
        self.ruta = ruta

    def obtenerDatos(self) -> str:
        """
        funcion para obtener datos
        """
        with open(self.ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)

        return datos


class MotorEmocional(ObtenerDatos):
    """
    Metodo para generar una emocion
    inicial
    """

    def __init__(self, ruta) -> None:
        super().__init__(ruta=ruta)
        self.mood = random.randint(0, len(self.obtenerDatos()) - 1)

    def getMood(self) -> str:
        """
        Obtener emocion
        """
        return self.obtenerDatos()[self.mood]  # pyright: ignore[reportIndexIssue]

    def getNewMood(self) -> str:
        """
        Obtener nueva emocion
        """
        self.mood = random.randint(0, len(self.obtenerDatos()) - 1)
        return self.obtenerDatos()[self.mood]  # pyright: ignore[reportIndexIssue]
