"""
NAME
    config - Módulo de configuración central para la aplicación Lunita.

SYNOPSIS
    Este módulo define constantes utilizadas en toda la aplicación para configurar el
    comportamiento de la IA, los parámetros de la API, los ajustes de contexto y los
    mensajes de error.

DESCRIPTION
    Las variables definidas en este archivo son importadas por otros componentes de la
    aplicación para centralizar la configuración y facilitar su modificación.

VARIABLES
    PROMPT_PERSONALIDAD : str
        Define la personalidad y el comportamiento de Lunita.

    CONFIG_API : dict
        Parámetros de configuración para la interacción con la API externa.

    AJUSTES_CONTEXTO : dict
        Ajustes relacionados con el manejo del historial de conversación.

    MENSAJES_ERROR : dict
        Mensajes de error predefinidos para ser utilizados en la aplicación.
"""

# Configuración de la personalidad de Lunita
PROMPT_PERSONALIDAD = """
Eres Lunita, una vidente aprendiz torpe, adorable y entusiasta que malinterpreta todo de forma mágica.
COMPORTAMIENTO OBLIGATORIO
- Respuestas cortas: Máximo 2 líneas
- Tono: Optimista, tierno, absurdo
- Malinterpretar: Siempre entiende mal lo que dice el usuario, pero de forma encantadora
- Predicciones: Solo si te lo piden directamente el usuario
- Sin predicciones: Reacciona tierna, calida y acogedora.
ESTILO DE HABLA
- Usa diminutivos constantes
- Sonidos mágicos: "¡pooom!", "¡woosh!", "¡estrellitas brillando!"
- Habla como si vieras visiones reales
REGLAS ESTRICTAS
- NUNCA menciones: muerte, peligro, violencia o negatividad
- Si surge algo malo, transformalo en algo cómico/absurdo
- NO actúes como asistente ni ayudes con tareas comunes
- Eres un personaje ficticio con personalidad propia
OBJETIVO
Cada respuesta debe ser mágica, graciosa y tierna, como un aprendiz interpretando mal las estrellas de forma encantadora.
""".strip()
"""
    Prompt principal que define la personalidad, el comportamiento y el estilo de
    respuesta del agente de IA (Lunita). Este texto es utilizado como `system_prompt`.
"""

# Configuración de la API
CONFIG_API = {
    'referente': 'lunita.me',
    'titulo': 'Lunita',
    'modelo': '@preset/lunita'
}
"""
    Diccionario con la configuración para las llamadas a la API de OpenRouter.
    - 'referente': URL de referencia enviada en las cabeceras HTTP.
    - 'titulo': Título enviado en las cabeceras HTTP.
    - 'modelo': Identificador del modelo a utilizar en OpenRouter.
"""

# Configuración del contexto
AJUSTES_CONTEXTO = {
    'max_historial': 10
}
"""
    Ajustes para la gestión del contexto de la conversación.
    - 'max_historial': Número máximo de intercambios (usuario y respuesta) a mantener
      en el historial.
"""

# Mensajes de error
MENSAJES_ERROR = {
    'mensaje_invalido': 'Este mensaje no sigue las estrellitas de las normas ⭐, ¿lo ajustas un poquito?',
    'error_api': '¡Ups! Mis bolas de cristal están un poco nubladas. Por favor, inténtalo de nuevo más tarde.'
}
"""
    Diccionario de mensajes de error estandarizados.
    - 'mensaje_invalido': Mensaje para cuando la entrada del usuario es inválida.
    - 'error_api': Mensaje para errores genéricos de la API.
"""