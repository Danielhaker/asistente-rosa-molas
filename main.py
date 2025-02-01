import os
from flask import Flask, request, jsonify, render_template, send_file, send_from_directory, session
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv
import time
import glob
from google.ai.generativelanguage_v1beta.types import content

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Necesario para las sesiones

# Configure Gemini AI with advanced settings
generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

# Initialize the model with the new configuration
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)

# Datos del colegio
HORARIO = {
    "Lunes": [
        {"hora": "8:10 - 9:05", "materia": "INGLÉS"},
        {"hora": "9:05 - 10:00", "materia": "RELIGIÓN"},
        {"hora": "10:00 - 10:55", "materia": "LENGUA CASTELLANA Y LITERATURA"},
        {"hora": "10:55 - 11:25", "materia": "RECREO"},
        {"hora": "11:25 - 12:20", "materia": "FRANCÉS"},
        {"hora": "12:20 - 13:15", "materia": "GEOGRAFÍA E HISTORIA"},
        {"hora": "13:15 - 15:00", "materia": "COMER"},
        {"hora": "15:00 - 15:55", "materia": "BIOLOGÍA Y GEOLOGÍA"},
        {"hora": "15:55 - 16:50", "materia": "MATEMÁTICAS"}
    ],
    "Martes": [
        {"hora": "8:10 - 9:05", "materia": "GEOGRAFÍA E HISTORIA"},
        {"hora": "9:05 - 10:00", "materia": "INGLÉS"},
        {"hora": "10:00 - 10:55", "materia": "ARTS"},
        {"hora": "10:55 - 11:25", "materia": "RECREO"},
        {"hora": "11:25 - 12:20", "materia": "P.E"},
        {"hora": "12:20 - 13:15", "materia": "MATEMÁTICAS"},
        {"hora": "13:15 - 15:00", "materia": "COMER"},
        {"hora": "15:00 - 15:55", "materia": "LENGUA CASTELLANA Y LITERATURA"},
        {"hora": "15:55 - 16:50", "materia": "ARTS"}
    ],
    "Miércoles": [
        {"hora": "8:10 - 9:05", "materia": "INGLÉS"},
        {"hora": "9:05 - 10:00", "materia": "BIOLOGÍA Y GEOLOGÍA"},
        {"hora": "10:00 - 10:55", "materia": "MUSIC"},
        {"hora": "10:55 - 11:25", "materia": "RECREO"},
        {"hora": "11:25 - 12:20", "materia": "MATEMÁTICAS"},
        {"hora": "12:20 - 13:15", "materia": "GEOGRAFÍA E HISTORIA"},
        {"hora": "13:15 - 15:00", "materia": "COMER"}
    ],
    "Jueves": [
        {"hora": "8:10 - 9:05", "materia": "TUTORÍA"},
        {"hora": "9:05 - 10:00", "materia": "BIOLOGÍA Y GEOLOGÍA"},
        {"hora": "10:00 - 10:55", "materia": "INGLÉS"},
        {"hora": "10:55 - 11:25", "materia": "RECREO"},
        {"hora": "11:25 - 12:20", "materia": "P.E"},
        {"hora": "12:20 - 13:15", "materia": "COMER"},
        {"hora": "15:00 - 15:55", "materia": "MUSIC"},
        {"hora": "15:55 - 16:50", "materia": "LENGUA CASTELLANA Y LITERATURA"}
    ],
    "Viernes": [
        {"hora": "8:10 - 9:05", "materia": "ARTS"},
        {"hora": "9:05 - 10:00", "materia": "FRANCÉS"},
        {"hora": "10:00 - 10:55", "materia": "MATEMÁTICAS"},
        {"hora": "10:55 - 11:25", "materia": "RECREO"},
        {"hora": "11:25 - 12:20", "materia": "LENGUA CASTELLANA Y LITERATURA"},
        {"hora": "12:20 - 13:15", "materia": "MUSIC"},
        {"hora": "13:15 - 15:00", "materia": "COMER"}
    ]
}

MENU = {
    "Lunes 6": "Festivo",
    "Martes 7": {
        "Primer plato": "Lentejas estofadas con cebolla, ajo, zanahoria y chorizo",
        "Segundo plato": "Croquetas de bacalao con ensalada de lechuga y maíz",
        "Postre": "Fruta"
    },
    "Miércoles 8": "Festivo",
    "Jueves 9": {
        "Primer plato": "Espaguetis con tomate",
        "Segundo plato": "Filete de cabezada en su jugo con ensalada de lechuga y zanahoria",
        "Postre": "Fruta"
    },
    "Viernes 10": {
        "Primer plato": "Acelgas con patata, zanahoria y jamón York",
        "Segundo plato": "Muslo de pollo asado en su jugo con ensalada de lechuga y zanahoria",
        "Postre": "Yogur"
    },
    "Lunes 13": {
        "Primer plato": "Arroz con chorizo y jamón York",
        "Segundo plato": "Limanda a la romana con ensalada de lechuga y maíz",
        "Postre": "Fruta"
    },
    "Martes 14": {
        "Primer plato": "Alubias blancas estofadas con cebolla, ajo, puerro y zanahoria",
        "Segundo plato": "Tortilla de jamón York con ensalada de lechuga y maíz",
        "Postre": "Fruta"
    },
    "Miércoles 15": {
        "Primer plato": "Judía verde con patata",
        "Segundo plato": "Cabezada de cerdo a la riojana con ensalada de lechuga y zanahoria",
        "Postre": "Fruta"
    },
    "Jueves 16": {
        "Primer plato": "Lentejas estofadas con cebolla, ajo y zanahoria",
        "Segundo plato": "Merluza en salsa verde (ajo, cebolla, perejil)",
        "Postre": "Fruta"
    },
    "Viernes 17": {
        "Primer plato": "Espaguetis a la italiana (cebolla, zanahoria, tomate)",
        "Segundo plato": "Pechuga de pollo a la milanesa con champiñón salteado",
        "Postre": "Flan"
    },
    "Lunes 20": {
        "Primer plato": "Arroz blanco con tomate frito",
        "Segundo plato": "Ventresca de merluza a la romana con lechuga",
        "Postre": "Fruta"
    },
    "Martes 21": {
        "Primer plato": "Crema de calabaza",
        "Segundo plato": "Muslo de pollo asado con ensalada",
        "Postre": "Fruta"
    },
    "Miércoles 22": {
        "Primer plato": "Garbanzos con chorizo, cebolla, pimiento y tomate",
        "Segundo plato": "Bacalao con tomate y pimientos asados",
        "Postre": "Fruta"
    },
    "Jueves 23": {
        "Primer plato": "Sopa casera de ave con fideos",
        "Segundo plato": "Tortilla de patata con ensalada de olivas, zanahoria y lechuga",
        "Postre": "Yogur"
    },
    "Viernes 24": {
        "Primer plato": "Brócoli con patata",
        "Segundo plato": "Hamburguesa casera de cerdo a la plancha con ensalada de lechuga y maíz",
        "Postre": "Fruta"
    },
    "Lunes 27": {
        "Primer plato": "Paella mixta (pollo, calamar, cebolla, tomate y pimiento)",
        "Segundo plato": "Tilapia a la romana con ensalada de lechuga y maíz",
        "Postre": "Fruta"
    },
    "Martes 28": {
        "Primer plato": "Puré de coliflor, calabacín y patata",
        "Segundo plato": "Pechuga de pollo a la plancha con pimientos rojos al horno",
        "Postre": "Fruta"
    },
    "Miércoles 29": "Festivo",
    "Jueves 30": {
        "Primer plato": "Espaguetis a la boloñesa (cebolla, zanahoria, tomate y carne)",
        "Segundo plato": "Merluza rebozada con ensalada de lechuga",
        "Postre": "Yogur"
    },
    "Viernes 31": {
        "Primer plato": "Alubias blancas con verduras (cebolla, zanahoria, calabacín)",
        "Segundo plato": "Lomo fresco a la plancha con patatas chips",
        "Postre": "Fruta"
    }
}

# Historial de conversación global
conversation_history = {}

def get_chat_history(session_id):
    return conversation_history.get(session_id, [])

def add_to_history(session_id, role, content):
    if session_id not in conversation_history:
        conversation_history[session_id] = []
    conversation_history[session_id].append({"role": role, "content": content})
    # Mantener solo las últimas 10 interacciones
    if len(conversation_history[session_id]) > 10:
        conversation_history[session_id].pop(0)

def clean_markdown(text):
    # Limpiar asteriscos de markdown
    text = text.replace('**', '')
    text = text.replace('*', '')
    # Limpiar otros símbolos de markdown comunes
    text = text.replace('`', '')
    text = text.replace('#', '')
    text = text.replace('>', '')
    text = text.replace('-', '')
    # Limpiar múltiples espacios
    text = ' '.join(text.split())
    return text

def generate_response(prompt, session_id):
    try:
        # Procesar preguntas sobre horario
        prompt_lower = prompt.lower()
        if "horario" in prompt_lower:
            if any(dia.lower() in prompt_lower for dia in HORARIO.keys()):
                for dia in HORARIO.keys():
                    if dia.lower() in prompt_lower:
                        horario_dia = HORARIO[dia]
                        response = f"El horario del {dia} es:\n"
                        for clase in horario_dia:
                            response += f"- {clase['hora']}: {clase['materia']}\n"
                        return response
            else:
                return "¿De qué día quieres saber el horario? Puedo decirte el horario de Lunes, Martes, Miércoles, Jueves o Viernes."

        # Procesar preguntas sobre el menú
        if "menu" in prompt_lower or "comer" in prompt_lower or "comida" in prompt_lower:
            if any(dia.lower() in prompt_lower for dia in MENU.keys()):
                for dia in MENU.keys():
                    if dia.lower() in prompt_lower:
                        menu_dia = MENU[dia]
                        if isinstance(menu_dia, str):
                            return f"El {dia} es {menu_dia}"
                        else:
                            response = f"El menú del {dia} es:\n"
                            for plato, descripcion in menu_dia.items():
                                response += f"- {plato}: {descripcion}\n"
                            return response
            else:
                dias_disponibles = ", ".join(MENU.keys())
                return f"¿De qué día quieres saber el menú? Tengo el menú de estos días: {dias_disponibles}"

        # Procesar preguntas sobre qué clase toca ahora
        if "que clase" in prompt_lower and "ahora" in prompt_lower:
            from datetime import datetime
            now = datetime.now()
            dia_semana = now.strftime("%A")
            hora_actual = now.strftime("%H:%M")
            
            # Mapear días en inglés a español
            dias_mapping = {
                "Monday": "Lunes",
                "Tuesday": "Martes",
                "Wednesday": "Miércoles",
                "Thursday": "Jueves",
                "Friday": "Viernes"
            }
            
            dia_espanol = dias_mapping.get(dia_semana)
            if dia_espanol in HORARIO:
                for clase in HORARIO[dia_espanol]:
                    hora_inicio = clase['hora'].split(' - ')[0]
                    hora_fin = clase['hora'].split(' - ')[1]
                    if hora_inicio <= hora_actual <= hora_fin:
                        return f"Ahora toca {clase['materia']} (de {clase['hora']})"
                return "No hay clase en este momento"
            else:
                return "Hoy no hay clases"

        # Si no es una pregunta específica sobre horario o menú, usar el modelo de Gemini
        history = get_chat_history(session_id)
        
        # Crear el contexto inicial del asistente
        initial_context = """Soy el asistente de los alumnos del colegio Rosa Molas. 
        Respondo en lenguaje natural y de forma amigable, sin usar formato JSON ni símbolos especiales."""
        
        # Crear el contexto con el historial
        context = f"{initial_context}\n\nBasándote en la siguiente conversación, proporciona una respuesta nueva y relevante:\n\n"
        for msg in history:
            context += f"{msg['role']}: {msg['content']}\n"
        
        # Agregar el nuevo prompt
        context += f"\nNueva pregunta: {prompt}\n\nResponde de forma directa y concisa, en lenguaje natural."
        
        response = model.generate_content(context)
        text = response.text.strip()
        
        # Limpiar la respuesta
        text = text.replace("Asistente:", "").replace("Assistant:", "").strip()
        text = clean_markdown(text)
        
        # Agregar al historial
        add_to_history(session_id, "user", prompt)
        add_to_history(session_id, "assistant", text)
        
        return text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Lo siento, ha ocurrido un error al procesar tu consulta. Por favor, inténtalo de nuevo."

def text_to_speech(text, lang='es'):
    try:
        # Generar un nombre único para el archivo de audio basado en el timestamp
        timestamp = int(time.time())
        audio_file = f"static/response_{timestamp}.mp3"
        
        # Eliminar archivos de audio antiguos
        cleanup_old_audio_files()
        
        tts = gTTS(text=text, lang=lang)
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None

def cleanup_old_audio_files():
    try:
        # Mantener solo los últimos 5 archivos de audio
        audio_files = glob.glob("static/response_*.mp3")
        if len(audio_files) > 5:
            # Ordenar por fecha de modificación
            audio_files.sort(key=os.path.getmtime)
            # Eliminar los más antiguos
            for file in audio_files[:-5]:
                os.remove(file)
    except Exception as e:
        print(f"Error cleaning up audio files: {e}")

@app.route('/')
def home():
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/query', methods=['POST'])
def query():
    try:
        if 'session_id' not in session:
            session['session_id'] = os.urandom(16).hex()
            
        data = request.json
        user_input = data.get('query', '')
        
        # Generate response using Gemini with session history
        response_text = generate_response(user_input, session['session_id'])
        
        # Convert response to speech
        audio_file = text_to_speech(response_text)
        
        if audio_file:
            return jsonify({
                'response': response_text,
                'audio_url': f'/{audio_file}'
            })
        else:
            return jsonify({
                'response': response_text,
                'error': 'Error generating audio'
            })
            
    except Exception as e:
        print(f"Error in query endpoint: {e}")
        return jsonify({
            'response': 'Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo.',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, host='0.0.0.0')