from bisect import bisect_right
from random import sample


def obtener_signo_zodiacal(dia: int, mes: int) -> dict[str, str]:
    """
    Determina el signo zodiacal basado en la fecha de nacimiento.
    """
    cortes = [120, 219, 321, 420, 521, 621, 723, 823, 923, 1023, 1122, 1222]

    signos = [
        {
            "Signo": "Umbra",
            "Personalidad": "Misteriositos, siempre aparecen cuando alguien se tapa la lámpara.",
            "Interpretación": "Lunita los ve como los que guardan los secretos bajo las cobijitas",
        },
        {
            "Signo": "Nova",
            "Personalidad": "Dramáticos, intensos, hacen todo con ¡Poooom!",
            "Interpretación": "Lunita los ve como los fuegos artificiales que nunca se apagan.",
        },
        {
            "Signo": "Pulsarín",
            "Personalidad": "Repetitivos, obsesivos, pero adorables, como un relojito cósmico.",
            "Interpretación": "Lunita dice que 'laten como un corazoncito galáctico'.",
        },
        {
            "Signo": "Quasín",
            "Personalidad": "Magnéticos, intensos, siempre atrayendo gente rara.",
            "Interpretación": "Para Lunita son 'farolitos cósmicos que guían a las abejitas espaciales'.",
        },
        {
            "Signo": "Negruna",
            "Personalidad": "Intensos, posesivos, absorben todo (incluido el postre).",
            "Interpretación": "Lunita cree que 'abrazan tan fuerte que nada se les escapa'.",
        },
        {
            "Signo": "Craterín",
            "Personalidad": "Nostálgicos, viven llenos de historias del pasado.",
            "Interpretación": "Lunita los adora porque 'guardan piedritas mágicas en sus bolsillitos'.",
        },
        {
            "Signo": "Cometín",
            "Personalidad": "Inquietos, nunca se quedan en un lugar, siempre con la maleta lista.",
            "Interpretación": "Lunita los ve como 'cabellitos con glitter que dejan estelitas al caminar'.",
        },
        {
            "Signo": "Nebulina",
            "Personalidad": "Dispersos, soñadores, viven en una nube literal.",
            "Interpretación": "Para Lunita son 'almohaditas de colores para descansar la mente'.",
        },
        {
            "Signo": "Eclipsona",
            "Personalidad": "Dramáticos y teatrales, aman el misterio y la sorpresa.",
            "Interpretación": "Lunita dice que 'apagan la luz solo para hacer juegos de escondiditas cósmicas'.",
        },
        {
            "Signo": "Asteroidecito",
            "Personalidad": "Testarudos, van por su camino aunque choquen con todo.",
            "Interpretación": "Lunita los describe como 'canicas espaciales que hacen ¡toc-toc! en el universo'.",
        },
        {
            "Signo": "Radiantín",
            "Personalidad": "Alegres, caóticos, llegan en grupo y nunca avisan.",
            "Interpretación": "Para Lunita son 'confeti de cumpleaños que cae del cielo cada noche'.",
        },
        {
            "Signo": "Espectrina",
            "Personalidad": "Profundos, sensibles, cambian de color con sus emociones.",
            "Interpretación": "Lunita los ve como 'arcoíris tímidos escondidos en un telescopio'.",
        },
    ]

    index = bisect_right(cortes, dia + mes * 100) - 1

    return signos[index] if index >= 0 else signos[-1]


def tarot() -> list[str]:
    """
    Selecciona tres cartas del tarot de manera aleatoria para una tirada básica.
    """

    cartas = [
        "El Loco",
        "El Mago",
        "La Sacerdotisa",
        "La Emperatriz",
        "El Emperador",
        "El Hierofante",
        "Los Amantes",
        "El Carro",
        "Fuerza",
        "El Ermitaño",
        "Rueda De La Fortuna",
        "Justicia",
        "El Colgado",
        "Muerte",
        "Templanza",
        "El Diablo",
        "La Torre",
        "La Estrella",
        "La Luna",
        "El Sol",
        "Juicio",
        "El Mundo",
        "Diez De Copas",
        "As De Copas",
        "Dos De Copas",
        "Tres De Copas",
        "Cuatro De Copas",
        "Cinco De Copas",
        "Seis De Copas",
        "Siete De Copas",
        "Ocho De Copas",
        "Nueve De Copas",
        "Rey De Copas",
        "Caballero De Copas",
        "Sota De Copas",
        "Reina De Copas",
        "Diez De Oros",
        "As De Oros",
        "Dos De Oros",
        "Tres De Oros",
        "Cuatro De Oros",
        "Cinco De Oros",
        "Seis De Oros",
        "Siete De Oros",
        "Ocho De Oros",
        "Nueve De Oros",
        "Rey De Oros",
        "Caballero De Oros",
        "Sota De Oros",
        "Reina De Oros",
        "Diez De Espadas",
        "As De Espadas",
        "Dos De Espadas",
        "Tres De Espadas",
        "Cuatro De Espadas",
        "Cinco De Espadas",
        "Seis De Espadas",
        "Siete De Espadas",
        "Ocho De Espadas",
        "Nueve De Espadas",
        "Rey De Espadas",
        "Caballero De Espadas",
        "Sota De Espadas",
        "Reina De Espadas",
        "Diez De Bastos",
        "As De Bastos",
        "Dos De Bastos",
        "Tres De Bastos",
        "Cuatro De Bastos",
        "Cinco De Bastos",
        "Seis De Bastos",
        "Siete De Bastos",
        "Ocho De Bastos",
        "Nueve De Bastos",
        "Rey De Bastos",
        "Caballero De Bastos",
        "Sota De Bastos",
        "Reina De Bastos",
    ]

    return sample(cartas, 3)


HERRAMIENTAS = [tarot, obtener_signo_zodiacal]
