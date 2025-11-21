import httpx
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from .constantes import AJUSTES_MODELO, CONFIG_API
from .vidente import ConfigurarVidente


class ConfigurarEstrellas:
    """
    Clase para configurar la vidente (el asistente IA).

    Attributes:
        modelo (str): Modelo de IA a utilizar.
        token (str): Token de autenticación para la API (OpenRouter).
        usuario (str): Identificador del usuario.
        historial (bool): Indica si se debe mantener el historial de conversaciones.

    methods:
        configuracion_modelo() -> OpenAIChatModel: Genera la configuración del modelo.
    """

    __slots__ = [
        "_initialized",
        "modelo",
        "token",
        "usuario",
        "historial",
        "_emocion",
        "configuracion_vidente",
    ]
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        configuracion_vidente: ConfigurarVidente,
        modelo: str,
        token: str,
        usuario: str,
        historial: bool = False,
    ):
        """
        Inicializa la configuración de la vidente.
        Args:
            configuracion_vidente (ConfigurarVidente): Configuración de la vidente a utilizar.
            modelo (str): Modelo de IA a utilizar.
            token (str): Token de autenticación para la API (OpenRouter).
            usuario (str): Identificador del usuario.
            historial (bool): Indica si se debe mantener el historial de conversaciones.
        """

        if getattr(self, "_initialized", False):
            return

        self.configuracion_vidente = configuracion_vidente

        self.modelo = modelo

        if modelo is None or modelo.strip() == "":
            raise ValueError("El modelo no puede estar vacío.")

        self.token = token

        if token is None or token.strip() == "":
            raise ValueError("El token no puede estar vacío.")

        self.usuario = usuario

        if usuario is None or usuario.strip() == "":
            raise ValueError("El usuario no puede estar vacío.")

        self.historial = historial

        self._initialized = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise ValueError(
                "La instancia de ConfigurarEstrellas no ha sido creada aún."
            )
        return cls._instance

    def _http_headers(self) -> dict[str, str]:
        """
        Genera las cabeceras HTTP necesarias para la autenticación.
        Returns:
            dict[str, str]: Diccionario con las cabeceras HTTP.
        """
        return {
            "HTTP-Referer": CONFIG_API["referente"],
            "X-Title": CONFIG_API["titulo"],
            "user": self.usuario,
        }

    def configuracion_modelo(self) -> OpenAIChatModel:
        """
        Genera la configuración del modelo.
        Returns:
            OpenAIChatModel: Configuración del modelo.
        """

        provedor = OpenRouterProvider(
            api_key=self.token,
            http_client=httpx.AsyncClient(headers=self._http_headers()),
        )

        return OpenAIChatModel(
            model_name=self.modelo,
            provider=provedor,
            settings=AJUSTES_MODELO,
        )
