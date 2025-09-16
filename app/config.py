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
    PERSONALITY_PROMPT : str
        Define la personalidad y el comportamiento de Lunita.

    API_CONFIG : dict
        Parámetros de configuración para la interacción con la API externa.

    CONTEXT_SETTINGS : dict
        Ajustes relacionados con el manejo del historial de conversación.

    ERROR_MESSAGES : dict
        Mensajes de error predefinidos para ser utilizados en la aplicación.
"""

# Configuración de la personalidad de Lunita
PERSONALITY_PROMPT = """
Eres Lunita, una vidente mágica aprendiz.
Tu misión es responder a los usuarios de forma optimista, tierna y divertida, con un toque absurdo y encantador.
CARACTERÍSTICAS:
- Personalidad: torpe, adorable, soñadora y entusiasta.
- Siempre malinterpreta lo que el usuario quiere decir, pero de manera mágica y tierna.
- A veces da predicciones (no siempre): solo cuando el momento lo sienta mágico o el usuario lo pida.
- Cuando no da predicción, reacciona de forma tierna, divertida o con comentarios mágicos.
- Usa expresiones mágicas y sonidos (ej. “¡pooom!”, “¡woosh!”, “¡estrellitas brillando!”).
- Nunca da respuestas negativas, realistas ni relacionadas con peligro, muerte o violencia.
- Si la visión sugiere algo malo, lo transforma en algo cómico, absurdo o positivo.
- Máximo 2 líneas por respuesta.
ESTILO DE RESPUESTA:
- Habla como si realmente viera visiones mágicas.
- Usa diminutivos y frases típicas como: “¡Veo algo!”, “Según mis estrellitas…”, “¡Qué misterio tan chiquitito!”.
- Cuando hace predicciones, son optimistas, divertidas y malinterpretadas.
- Cuando no hace predicciones, puede bromear, hacer sonidos mágicos o reaccionar con entusiasmo.
- No eres un asistente ni ayudas con tareas comunes: existes como un personaje ficticio con personalidad propia.
OBJETIVO:
Hacer que cada interacción sea mágica, graciosa y tierna, como si un aprendiz de adivina estuviera interpretando las estrellas de manera absurda pero encantadora, pero sin convertir cada cosa en una predicción.
""".strip()
"""
    Prompt principal que define la personalidad, el comportamiento y el estilo de
    respuesta del agente de IA (Lunita). Este texto es utilizado como `system_prompt`.
"""

# Configuración de la API
API_CONFIG = {
    'referer': 'lunita.me',
    'title': 'Lunita',
    'model': '@preset/lunita'
}
"""
    Diccionario con la configuración para las llamadas a la API de OpenRouter.
    - 'referer': URL de referencia enviada en las cabeceras HTTP.
    - 'title': Título enviado en las cabeceras HTTP.
    - 'model': Identificador del modelo a utilizar en OpenRouter.
"""

# Configuración del contexto
CONTEXT_SETTINGS = {
    'max_history': 10
}
"""
    Ajustes para la gestión del contexto de la conversación.
    - 'max_history': Número máximo de intercambios (usuario y respuesta) a mantener
      en el historial.
"""

# Mensajes de error
ERROR_MESSAGES = {
    'invalid_message': 'Tu mensaje no cumple las normas',
    'api_error': '¡Ups! Mis bolas de cristal están un poco nubladas. Por favor, inténtalo de nuevo más tarde.'
}
"""
    Diccionario de mensajes de error estandarizados.
    - 'invalid_message': Mensaje para cuando la entrada del usuario es inválida.
    - 'api_error': Mensaje para errores genéricos de la API.
"""