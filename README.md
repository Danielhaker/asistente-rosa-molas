# Asistente Rosa Molas

Un asistente virtual inteligente para el Colegio Rosa Molas, desarrollado con Flask y la API de Gemini.

## Características

- Interfaz de chat intuitiva
- Respuestas generadas por IA utilizando Gemini
- Capacidad de texto a voz
- Diseño responsive y moderno
- PWA (Progressive Web App) compatible

## Requisitos

- Python 3.12+
- Flask
- gTTS (Google Text-to-Speech)
- API Key de Gemini

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/asistente-rosa-molas.git
cd asistente-rosa-molas
```

2. Crea un entorno virtual e instala las dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Crea un archivo `.env` con tu API key de Gemini:
```
GEMINI_API_KEY=tu-api-key
```

4. Ejecuta la aplicación:
```bash
python main.py
```

La aplicación estará disponible en `http://localhost:5000`

## Uso

1. Abre la aplicación en tu navegador
2. Escribe tu pregunta en el campo de texto
3. Presiona "Enviar" o usa el botón del micrófono para entrada por voz
4. El asistente responderá a tus preguntas sobre el colegio
