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