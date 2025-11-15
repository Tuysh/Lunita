# 🌙 Lunita

> Un asistente de IA emocionalmente consciente

Lunita es un compañero digital que comprende y responde a las emociones.
## Características

- **🔮 Personalidad Dinámica** — Respuestas espontáneas y cambios de humor
- **🎯 Herramientas Integradas** — Lectura de tarot, signos de zodiaco
- **⚡ API Moderna** — Construida con Pydantic AI y Mistral AI

## Instalación

**Como paquete (recomendado):**

```bash
pip install git+https://github.com/CualliLabs/Lunita.git
```

**Desde el código fuente:**

```bash
git clone https://github.com/CualliLabs/Lunita.git
cd Lunita
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Configuración:**

Crea un archivo `.env` con tu token de Mistral:

```env
MINISTRAL_TOKEN=tu_token_aqui
```

## Uso

```python
import asyncio
import os
from dotenv import load_dotenv
from lunita import Lunita

load_dotenv()

async def main():
    lunita = Lunita(token=os.getenv("MINISTRAL_TOKEN"), usuario="user_1")

    while True:
        pregunta = input("Tú: ")
        if pregunta.lower() == "exit":
            break

        respuesta = await lunita.predecir(pregunta)
        print(f"\nLunita: {respuesta}\n")

        estado = lunita.obtener_estado()
        print(f"Emoción: {estado['emocion_actual']}\n")

if __name__ == "__main__":
    asyncio.run(main())
```

## Estructura

```
lunita/
├── lunita.py          # Clase principal
├── cliente.py         # Cliente Mistral AI
├── emocional.py       # Motor emocional
├── herramientas.py    # Herramientas integradas
├── utilidades.py      # Funciones auxiliares
├── configuracion.py   # Configuración
└── data/              # Datos de emociones y personalidad
```

## Tecnologías

- **[Pydantic AI](https://ai.pydantic.dev/)** — Framework de IA con validación de tipos
- **[Mistral AI](https://mistral.ai/)** — Modelo de lenguaje
- **Python 3.8+**

## Licencia

MIT — Consulta el archivo `LICENSE` para más detalles.

---

Hecho con ❤️ por **Cualli Labs**
