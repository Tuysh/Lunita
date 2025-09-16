# 🌙 Lunita Core

El núcleo de un asistente digital emocionalmente consciente.

Lunita es un proyecto diseñado para ser un compañero emocional. Su propósito es comprender, procesar y responder a las emociones, actuando como un guardián digital amigable.

## ✨ Características

*   **Análisis Emocional:** Capaz de interpretar y clasificar emociones a partir de texto.
*   **Módulo Guardián:** Provee una capa de seguridad y control en las interacciones.
*   **Arquitectura Flexible:** Componentes modulares para una fácil expansión.

## 🚀 Puesta en Marcha

Sigue estos pasos para poner en funcionamiento el núcleo de Lunita.

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/CualliLabs/Lunita.git
    cd Lunita
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
    ```
    pip install -r requirements.txt
    ```

4.  **Ejecuta la aplicación:**
    ```bash
    python main.py
    ```

## 📂 Estructura del Proyecto

```
core/
├── app/                # Contiene la lógica principal de la aplicación.
│   ├── Lunita.py       # El núcleo del asistente.
│   ├── Emocional.py    # Manejo y análisis de emociones.
│   ├── Guardian.py     # Módulo de seguridad y supervisión.
│   ├── Client.py       # Lógica para la interacción con el cliente.
│   └── json/
│       └── emociones.json # Datos relacionados con las emociones.
├── main.py             # Punto de entrada de la aplicación.
├── .gitignore          # Archivos ignorados por Git.
├── LICENSE             # Licencia del proyecto.
├── example.env         # Variables de entorno de ejemplo.
├── .editorconfig       # Configuración del editor.
├── requirements.txt    # Dependencias del proyecto.
└── README.md           # Este archivo.
```

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo `LICENSE` para más detalles.

---
Hecho con ❤️ por Cualli Labs
