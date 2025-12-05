# 🛠 Guía Técnica y de Contribución

¡Gracias por tu interés en profundizar en la magia de Lunita! Aquí encontrarás los detalles técnicos para instalar, configurar y desarrollar con el SDK.

## 🚀 Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/CualliLabs/Lunita.git
   cd Lunita
   ```

2. **Entorno Virtual**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\Activate.ps1
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuración**:
   Crea un archivo `.env` con tu token de API (OpenRouter):
   ```env
   LUNITA_TOKEN=tu_token_aqui
   ```

## 🔮 Uso del SDK

Lunita está diseñada para ser intuitiva. Aquí tienes un ejemplo de cómo invocarla:

```python
import asyncio
import os
from lunita import ConfigurarVidente, ConfigurarEstrellas, Sesion

async def main():
    # 1. Configura la personalidad
    vidente = ConfigurarVidente(vidente="lunita")

    # 2. Conecta con las estrellas
    ConfigurarEstrellas(
        usuario="dev_user",
        modelo="x-ai/grok-4.1-fast",
        api_token=os.getenv("LUNITA_TOKEN"),
        configuracion_vidente=vidente,
        historial=True
    )

    # 3. Inicia la sesión
    sesion = Sesion()

    # 4. Interactúa
    print("✨ Iniciando sesión con Lunita...")
    respuesta = await sesion.predecir("Hola Lunita, ¿cómo te sientes hoy?")
    print(f"\nLunita: {respuesta.texto}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🛠 Tecnologías

- **[Pydantic AI](https://ai.pydantic.dev/)**: El corazón estructurado de nuestros agentes.
- **OpenRouter**: La puerta a los modelos de lenguaje.
- **Python 3.10+**: Nuestro hechizo base.

---
Si deseas contribuir con código, por favor abre un Pull Request o un Issue para discutir tus ideas. ¡Toda magia es bienvenida!
