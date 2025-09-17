import random

from .utilidades import CargadorDatos


class MotorEmocional(CargadorDatos):
    """
    NAME
        MotorEmocional - Gestiona el estado emocional de Lunita.

    SYNOPSIS
        - me = MotorEmocional(ruta)
        - me.obtener_emocion() -> str
        - me.obtener_nueva_emocion() -> str

    DESCRIPTION
        Hereda de `CargadorDatos` para cargar una lista de emociones desde un archivo
        JSON y proporciona métodos para obtener una emoción aleatoria, ya sea la
        actual o una nueva.

    ATTRIBUTES
        emocion_actual : int
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
        self.emocion_actual = random.randint(0, len(self.cargar_datos()) - 1)

    def obtener_emocion(self) -> str:
        """Obtiene la emoción actual.

        RETURN VALUES
            str
                La cadena de texto que representa la emoción actual.
        """
        return self.cargar_datos()[self.emocion_actual]

    def obtener_nueva_emocion(self) -> str:
        """Selecciona y devuelve una nueva emoción aleatoria.

        SIDE EFFECTS
            Modifica el atributo `self.emocion_actual` a un nuevo valor aleatorio.

        RETURN VALUES
            str
                La cadena de texto de la nueva emoción seleccionada.
        """
        self.emocion_actual = random.randint(0, len(self.cargar_datos()) - 1)
        return self.cargar_datos()[self.emocion_actual]
