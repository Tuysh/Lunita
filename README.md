# 🌙 Lunita SDK

> Tu amiga vidente y asistente emocionalmente consciente.

Lunita no es solo un chatbot; es una compañera digital con "sentimientos". Su estado emocional cambia dinámicamente según la conversación, afectando sus respuestas y personalidad. Vive en un mundo mágico, lee el tarot y siempre busca hacerte sonreír.

## ✨ Características

- **🔮 Personalidad Dinámica** — Sus emociones cambian y afectan sus respuestas.
- **🎯 Herramientas Mágicas** — Lectura de tarot y horóscopos integrados.
- **⚡ Tecnología Moderna** — Construida sobre Pydantic AI y modelos LLM avanzados.

## 🚀 Instalación

1. Clona el repositorio y entra en la carpeta:
   ```bash
   git clone https://github.com/CualliLabs/Lunita.git
   cd Lunita
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\Activate.ps1
   # Linux/Mac
   source venv/bin/activate

   pip install -r requirements.txt
   ```

3. Configura tu entorno:
   Crea un archivo `.env` (o configura variables de entorno) con tu token de API (OpenRouter):
   ```env
   LUNITA_TOKEN=tu_token_aqui
   ```

## 🔮 Uso Básico

El nuevo SDK de Lunita está diseñado para ser intuitivo y flexible. Aquí tienes un ejemplo completo:

```python
import asyncio
import os
from lunita import ConfigurarVidente, ConfigurarEstrellas, Sesion

async def main():
    # 1. Configura la personalidad de tu vidente
    vidente = ConfigurarVidente(vidente="lunita")

    # 2. Conecta con las estrellas (Configuración de API)
    ConfigurarEstrellas(
        usuario="user_1",
        modelo="x-ai/grok-4.1-fast",
        api_token=os.getenv("LUNITA_TOKEN"),
        configuracion_vidente=vidente,
        historial=True
    )

    # 3. Inicia la sesión mágica
    sesion = Sesion()

    # 4. ¡Interactúa!
    print("✨ Iniciando sesión con Lunita...")
    respuesta = await sesion.predecir("Hola Lunita, ¿qué dicen las cartas hoy?")

    print(f"\nLunita: {respuesta.text}")

    # 5. Consultar historial
    historial = sesion.consultas()

if __name__ == "__main__":
    asyncio.run(main())
```

## 🧩 Estructura del Proyecto

El núcleo de Lunita se organiza de la siguiente manera:

- **`lunita/vidente.py`**: Configuración de la personalidad y prompts del sistema.
- **`lunita/estrellas.py`**: Configuración de la infraestructura, API y parámetros técnicos.
- **`lunita/sesion.py`**: Gestión de la interacción, estado emocional y ciclo de vida de la conversación.
- **`lunita/emocional.py`**: Motor de emociones que simula estados de ánimo.
- **`lunita/herramientas.py`**: Implementación de herramientas mágicas (tarot, signos).

## 🛠 Tecnologías

- **[Pydantic AI](https://ai.pydantic.dev/)**: Validación robusta y estructura de agentes.
- **OpenRouter**: Modelos de lenguaje subyacentes.
- **Python 3.10+**: Desarrollado para entornos modernos.

---

Hecho con ❤️
