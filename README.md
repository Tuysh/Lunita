# 🌙 Lunita Core

El núcleo de un asistente de IA emocionalmente consciente con capacidades de memoria afectiva.

Lunita es un proyecto diseñado para ser un compañero emocional interactivo. Su propósito es comprender, procesar y responder a las emociones, actuando como un asistente digital amigable con memoria a largo plazo que aprende de cada conversación.

## ✨ Características

*   **🧠 Análisis Emocional:** Motor emocional capaz de interpretar y clasificar emociones a partir de texto.
*   **🛡️ Módulo Guardián:** Capa de seguridad y moderación en las interacciones usando SpanLP.
*   **💭 Memoria Afectiva:** Sistema de memoria con búsqueda semántica mediante IA que permite recordar conversaciones previas.
*   **🔮 Personalidad Dinámica:** Comportamiento proactivo con respuestas espontáneas y cambios de humor.
*   **🎯 Herramientas Integradas:** Soporte para acciones como búsqueda web, generación de imágenes y más.
*   **📊 Perfil de Usuario:** Construcción automática de perfil del usuario basado en las interacciones.
*   **⚡ API Moderna:** Basada en Pydantic AI con soporte para Mistral AI.

## 🚀 Instalación

### Como Paquete (Recomendado)

```bash
pip install git+https://github.com/CualliLabs/Lunita.git
```

### Desde el Código Fuente

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/CualliLabs/Lunita.git
    cd Lunita/core
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura tus variables de entorno:**

    Crea un archivo `.env` con tu token de Mistral AI:
    ```
    MISTRAL_API_KEY=tu_token_aqui
    ```

## 💻 Uso Básico

```python
import asyncio
from lunita import Lunita

async def main():
    # Inicializar Lunita
    lunita = Lunita(
        token="tu_token_mistral",
        usuario="nombre_usuario"
    )

    # Conversar con Lunita
    respuesta = await lunita.predecir("¡Hola! ¿Cómo estás?")
    print(respuesta)

    # Obtener estado emocional
    estado = lunita.obtener_estado_detallado()
    print(f"Emoción actual: {estado['emocion_actual']}")

    # Cerrar recursos
    await lunita.cerrar()

if __name__ == "__main__":
    asyncio.run(main())
```

Ver [ejemplo.py](ejemplo.py) para un ejemplo más completo.

## 📂 Estructura del Proyecto

```
core/
├── lunita/              # Paquete principal de la aplicación
│   ├── __init__.py      # Exporta la clase Lunita
│   ├── lunita.py        # Clase principal del asistente
│   ├── cliente.py       # Cliente para la API de Mistral
│   ├── emocional.py     # Motor de análisis emocional
│   ├── guardian.py      # Módulo de moderación y seguridad
│   ├── memoria.py       # Sistema de memoria afectiva
│   ├── herramientas.py  # Definición de herramientas (búsqueda, etc.)
│   ├── utilidades.py    # Funciones auxiliares
│   ├── configuracion.py # Configuración y constantes
│   └── json/            # Archivos de datos
│       ├── emociones.json
│       └── respuestas_espontaneas.json
├── ejemplo.py           # Ejemplo de uso
├── pyproject.toml       # Configuración del paquete
├── requirements.txt     # Dependencias del proyecto
├── MANIFEST.in          # Archivos adicionales para la distribución
├── LICENSE              # Licencia MIT
└── README.md            # Este archivo
```

## 🔧 Tecnologías

- **[Pydantic AI](https://ai.pydantic.dev/)**: Framework para aplicaciones de IA con validación de tipos
- **[Mistral AI](https://mistral.ai/)**: Modelo de lenguaje principal
- **[SpanLP](https://spanlp.readthedocs.io/)**: Análisis de lenguaje natural para moderación
- **[httpx](https://www.python-httpx.org/)**: Cliente HTTP asíncrono
- **Python 3.8+**: Lenguaje de programación

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo `LICENSE` para más detalles.

---
Hecho con ❤️ por Cualli Labs
