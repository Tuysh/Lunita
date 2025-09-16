
"""
NAME
    tipos - Módulo para la definición de alias de tipos personalizados.

DESCRIPTION
    Este módulo centraliza la definición de alias de tipos (TypeAlias) para mejorar
    la legibilidad y el mantenimiento del código en otras partes de la aplicación.
"""

from typing import TypeAlias

from openai.types.chat import ChatCompletionMessageParam

TipoMensaje: TypeAlias = ChatCompletionMessageParam
"""
Alias para el tipo `ChatCompletionMessageParam` de la biblioteca de OpenAI.

DESCRIPTION
    Este tipo representa la estructura de un mensaje que puede ser enviado a la API
    de chat de OpenAI, facilitando la anotación de tipos en funciones y métodos
    que manejan estos objetos.
"""
