# 🌙 Lunita Core

El núcleo de un asistente de IA emocionalmente consciente.

Lunita es un proyecto diseñado para ser un compañero emocional interactivo. Su propósito es comprender, procesar y responder a las emociones, actuando como un asistente digital amigable con memoria a largo plazo que aprende de cada conversación.

## ✨ Características

*   **🧠 Análisis Emocional:** Motor emocional capaz de interpretar y clasificar emociones a partir de texto.
*   **🛡️ Módulo Guardián:** Capa de seguridad y moderación en las interacciones usando SpanLP.
*   **🔮 Personalidad Dinámica:** Comportamiento proactivo con respuestas espontáneas y cambios de humor.
*   **🎯 Herramientas Integradas:** Soporte para acciones como búsqueda web, generación de imágenes y más.
*   **📊 Perfil de Usuario:** Construcción automática de perfil del usuario basado en las interacciones.
*   **⚡ API Moderna:** Basada en Pydantic AI con soporte para Mistral AI.

## 🚀 Instalación

### Como paquete (recomendado)

```bash
pip install git+https://github.com/CualliLabs/Lunita.git
```

### Desde el código fuente

1. Clona el repositorio:

```bash
git clone https://github.com/CualliLabs/Lunita.git
cd Lunita
```

2. Crea y activa un entorno virtual:

```powershell
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias:

```powershell
pip install -r requirements.txt
```

4. Configura tus variables de entorno:

Crea un archivo `.env` en la raíz del proyecto y define tu token del proveedor Mistral. El código actual espera la variable `MINISTRAL_TOKEN`:

```
MINISTRAL_TOKEN=tu_token_aqui
```

## 💻 Ejemplo de uso (actualizado)

El paquete expone la clase `Lunita` en `lunita`. La API principal es asíncrona: `predecir(mensaje: str) -> str`.

Aquí tienes un ejemplo mínimo que coincide con `ejemplo.py` incluido en el repositorio. Usa `python`/`PowerShell` para ejecutarlo después de configurar `.env`.

```python
import asyncio
import os
from dotenv import load_dotenv

from lunita import Lunita

load_dotenv()

TOKEN = os.getenv("MINISTRAL_TOKEN")
if not TOKEN:
    raise RuntimeError("La variable MINISTRAL_TOKEN no está definida en el entorno.")


async def main():
    # Crear la instancia de Lunita
    lunita = Lunita(token=TOKEN, usuario="user_1")

    try:
        while True:
            pregunta = input("Pregunta (o 'exit' para salir): ")
            if pregunta.strip().lower() == "exit":
                break

            respuesta = await lunita.predecir(pregunta)
            print("\nRespuesta:\n", respuesta)

            # Ejemplo de uso de utilidades disponibles
            estado = lunita.obtener_estado()
            print(f"Emoción actual: {estado['emocion_actual']} — total mensajes: {estado['total_mensajes']}")

    finally:
        # Lunita no expone un "cerrar" global; si usas el cliente directamente asegúrate
        # de cerrar recursos HTTP si los expones (httpx.AsyncClient). En la versión
        # actual, no es necesario llamar a `cerrar()`.
        pass


if __name__ == "__main__":
    asyncio.run(main())
```

También puedes revisar `ejemplo.py` en la raíz del proyecto para una versión idéntica del bucle interactivo.

## 📂 Estructura del proyecto

```
core/
├── lunita/              # Paquete principal de la aplicación
│   ├── __init__.py      # Exporta la clase Lunita
│   ├── lunita.py        # Clase principal del asistente
│   ├── cliente.py       # Cliente para la API de Mistral
│   ├── emocional.py     # Motor de análisis emocional
│   ├── herramientas.py  # Definición de herramientas (búsqueda, etc.)
│   ├── utilidades.py    # Funciones auxiliares
│   ├── configuracion.py # Configuración y constantes
│   └── data/            # Archivos de datos
│       ├── cartas.json
│       ├── emociones.json
│       └── signos.json
├── ejemplo.py           # Ejemplo de uso (interactivo)
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
- **[Pydantic AI](https://ai.pydantic.dev/)**: Framework para aplicaciones de IA con validación de tipos
- **[Mistral AI](https://mistral.ai/)**: Modelo de lenguaje principal
- **[SpanLP](https://spanlp.readthedocs.io/)**: Análisis de lenguaje natural para moderación
- **[httpx](https://www.python-httpx.org/)**: Cliente HTTP asíncrono
- **Python 3.8+**: Lenguaje de programación

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo `LICENSE` para más detalles.

---
Hecho con ❤️ por Cualli Labs
