import json
import random


class ObtenerDatos:
    """
    NAME
        ObtenerDatos - Clase base para la carga de datos desde un archivo JSON.

    SYNOPSIS
        - od = ObtenerDatos(ruta)
        - od.obtenerDatos() -> dict

    DESCRIPTION
        Esta clase proporciona una funcionalidad simple para leer un archivo JSON desde
        una ruta específica y devolver su contenido como un objeto de Python.
    """

    def __init__(self, ruta: str) -> None:
        """Inicializa la instancia con la ruta al archivo de datos.

        PARAMETERS
            ruta
                Ruta al archivo JSON que se va a leer.
        """
        self.ruta = ruta

    def obtenerDatos(self) -> dict:
        """Lee y decodifica el archivo JSON.

        RETURN VALUES
            dict
                Un diccionario que representa el contenido del archivo JSON.

        ERRORS
            Puede lanzar `FileNotFoundError` si la ruta no es válida o `json.JSONDecodeError`
            si el archivo no contiene un JSON válido.
        """
        with open(self.ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return datos


class MotorEmocional(ObtenerDatos):
    """
    NAME
        MotorEmocional - Gestiona el estado emocional de Lunita.

    SYNOPSIS
        - me = MotorEmocional(ruta)
        - me.getMood() -> str
        - me.getNewMood() -> str

    DESCRIPTION
        Hereda de `ObtenerDatos` para cargar una lista de emociones desde un archivo
        JSON y proporciona métodos para obtener una emoción aleatoria, ya sea la
        actual o una nueva.

    ATTRIBUTES
        mood : int
            Índice numérico que representa la emoción actual en la lista de emociones.
    """

    def __init__(self, ruta: str) -> None:
        """Inicializa el motor emocional.

        DESCRIPTION
            Llama al constructor de la clase base con la ruta del archivo y establece
            un estado de ánimo inicial seleccionando un índice aleatorio de la lista
            de emociones cargada.

        PARAMETERS
            ruta
                Ruta al archivo JSON que contiene la lista de emociones.
        """
        super().__init__(ruta=ruta)
        self.mood = random.randint(0, len(self.obtenerDatos()) - 1)

    def getMood(self) -> str:
        """Obtiene la emoción actual.

        RETURN VALUES
            str
                La cadena de texto que representa la emoción actual.
        """
        return self.obtenerDatos()[self.mood]

    def getNewMood(self) -> str:
        """Selecciona y devuelve una nueva emoción aleatoria.

        SIDE EFFECTS
            Modifica el atributo `self.mood` a un nuevo valor aleatorio.

        RETURN VALUES
            str
                La cadena de texto de la nueva emoción seleccionada.
        """
        self.mood = random.randint(0, len(self.obtenerDatos()) - 1)
        return self.obtenerDatos()[self.mood]