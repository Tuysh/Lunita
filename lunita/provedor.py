from typing import Type, TypeVar, Any, overload

import httpx
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.mistral import MistralProvider
from pydantic_ai.providers.openrouter import OpenRouterProvider


from .constantes import AJUSTES_MODELO, CONFIG_API

T = TypeVar("T")
M = TypeVar("M")


def obtener_proveedor_generico(
    token: str, proveedor_tipo: Type[T], http_client: httpx.AsyncClient
) -> T:
    """
    NAME
        obtener_proveedor_generico - Crea una instancia genérica de proveedor.

    SYNOPSIS
        - proveedor = obtener_proveedor_generico(token, proveedor_tipo)

    DESCRIPTION
        Crea y devuelve una instancia de proveedor configurada con el token
        proporcionado para interactuar con los modelos a través de OpenRouter.

    PARAMETERS
        token : str
            Token de API para autenticar las solicitudes al proveedor.

        proveedor_tipo : T
            Tipo de proveedor a instanciar (por ejemplo, MistralProvider,
            OpenRouterProvider).

    RETURNS
        T
            Instancia configurada del proveedor especificado.

    SEE ALSO
        `pydantic_ai.providers`.
    """
    return proveedor_tipo(api_key=token, http_client=http_client)  # type: ignore


@overload
def obtener_modelo_generico(
    proveedor: MistralProvider, modelo_tipo: type[MistralModel]
) -> MistralModel: ...


@overload
def obtener_modelo_generico(
    proveedor: OpenRouterProvider, modelo_tipo: type[OpenAIChatModel]
) -> OpenAIChatModel: ...


def obtener_modelo_generico(proveedor: Any, modelo_tipo: Any) -> Any:
    """
    NAME
        obtener_modelo_generico - Crea una instancia genérica de modelo.

    SYNOPSIS
        - modelo = obtener_modelo_generico(proveedor, modelo_tipo)

    DESCRIPTION
        Crea y devuelve una instancia de modelo utilizando el proveedor
        proporcionado para interactuar con los modelos a través de OpenRouter.

    PARAMETERS
        proveedor : T
            Instancia de proveedor para autenticar las solicitudes al modelo.

        modelo_tipo : T
            Tipo de modelo a instanciar (por ejemplo, MistralModel,
            OpenAIChatModel).

    RETURNS
        T
            Instancia configurada del modelo especificado.

    SEE ALSO
        `pydantic_ai.models`.
    """
    return modelo_tipo(
        model_name=CONFIG_API["modelo"],
        provider=proveedor,
        settings=AJUSTES_MODELO,
    )


def configurar_modelo(
    tipo_modelo: str, token: str, usuario: str, http_client: httpx.AsyncClient
) -> MistralModel | OpenAIChatModel:
    if tipo_modelo == "mistral":
        proveedor = obtener_proveedor_generico(token, MistralProvider, http_client)
        modelo = obtener_modelo_generico(proveedor, MistralModel)
    elif tipo_modelo == "openrouter":
        proveedor = obtener_proveedor_generico(token, OpenRouterProvider, http_client)
        modelo = obtener_modelo_generico(proveedor, OpenAIChatModel)
    else:
        raise ValueError(f"Tipo de modelo no soportado: {tipo_modelo}")
    return modelo
