import json

class CargadorDatos:
    """
    NAME
        CargadorDatos - Clase base para la carga de datos desde un archivo JSON.

    SYNOPSIS
        - cd = CargadorDatos(ruta)
        - cd.cargar_datos() -> dict

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

    def cargar_datos(self) -> dict:
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
