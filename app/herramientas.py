from bisect import bisect_right
from random import sample

from .utilidades import CargadorDatos


def obtener_signo_zodiacal(dia: int, mes: int) -> dict[str, str]:
    """
    Determina el signo zodiacal basado en la fecha de nacimiento.
    """
    cortes = [120, 219, 321, 420, 521, 621, 723, 823, 923, 1023, 1122, 1222]
    cd = CargadorDatos(ruta="./app/json/signos.json")
    signos = cd.cargar_datos()

    index = bisect_right(cortes, dia + mes * 100) - 1

    return signos[index] if index >= 0 else signos[-1]


def tarot() -> list[str]:
    """
    Selecciona tres cartas del tarot de manera aleatoria para una tirada básica.
    """
    cd = CargadorDatos(ruta="./app/json/cartas.json")
    cartas = cd.cargar_datos()

    return sample(cartas, 3)


HERRAMIENTAS = [tarot, obtener_signo_zodiacal]
