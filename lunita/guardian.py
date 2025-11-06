import logging

import httpx

logger = logging.getLogger(__name__)


class Guardian:
    """
    NAME
        Guardian - Clase para la moderación de contenido.

    SYNOPSIS
        - g = Guardian()
        - g.obtener_veredicto(message) -> bool

    DESCRIPTION
        Esta clase se encarga de analizar los mensajes de los usuarios para determinar
        si cumplen con las directrices de contenido. Utiliza un método interno que
        se espera que interactúe con una API de moderación.
    """

    CATEGORIAS_BLOQUEADAS = {
        "sexual",
        "hate_and_discrimination",
        "violence_and_threats",
        "dangerous_and_criminal_content",
        "selfharm",
    }

    def __init__(self, token: str):
        self.token = token
        self.http_client = httpx.AsyncClient(
            timeout=10.0,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

    async def obtener_veredicto(self, mensaje: str) -> bool:
        """Determina si un mensaje es apropiado según las directrices.

        DESCRIPTION
            Analiza el mensaje utilizando el detector de palabrotas y devuelve
            `True` si el mensaje no contiene palabrotas, lo que indica que es
            apropiado.

        PARAMETERS
            message
                El mensaje del usuario a verificar.

        RETURN VALUES
            bool
                `True` si el mensaje es apropiado, `False` si ha sido marcado como
                inapropiado.
        """
        try:
            if not mensaje or not isinstance(mensaje, str):
                return False

            response = await self.http_client.post(
                "https://api.mistral.ai/v1/moderations",
                json={"model": "mistral-moderation-latest", "input": [mensaje.strip()]},
            )

            if response.status_code != 200:
                logger.error(f"Error en API de moderación: {response.status_code}")
                # En caso de error, ser conservador y rechazar
                return False

            data = response.json()

            if not data.get("results"):
                logger.warning("No se recibieron resultados de moderación")
                return False

            resultado = data["results"][0]
            categorias = resultado.get("categories", {})

            # Verificar si alguna categoría bloqueada está activa
            for categoria in self.CATEGORIAS_BLOQUEADAS:
                if categorias.get(categoria, False):
                    logger.warning(
                        f"Mensaje inapropiado detectado - Categoría: {categoria}"
                    )
                    return False

            # Si no se activó ninguna categoría bloqueada, el mensaje es apropiado
            return True

        except Exception as e:
            logger.error(f"Error en Guardian.obtener_veredicto: {e}")
            # En caso de error, ser conservador y rechazar
            return False

    def analizar_contenido(self, mensaje: str) -> dict:
        """Análisis más detallado del contenido (para futuras mejoras)"""
        return {
            "es_apropiado": self.obtener_veredicto(mensaje),
            "longitud": len(mensaje),
            "palabras": len(mensaje.split()) if mensaje else 0,
        }
