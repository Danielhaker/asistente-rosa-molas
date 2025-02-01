const responses = {
    // Horarios
    "horario": "El horario general del colegio es:\n- Mañanas: 9:00 - 13:00\n- Tardes: 15:00 - 17:00",
    "hora entrada": "La hora de entrada es a las 9:00 de la mañana",
    "hora salida": "La hora de salida es a las 17:00",
    
    // Comedor
    "menu": "El menú de esta semana incluye:\nLunes: Pasta con tomate\nMartes: Lentejas\nMiércoles: Arroz con pollo\nJueves: Pescado con ensalada\nViernes: Pizza",
    "comedor": "El servicio de comedor está disponible de 13:00 a 15:00",
    
    // Actividades
    "actividades extraescolares": "Ofrecemos varias actividades extraescolares:\n- Deportes: fútbol, baloncesto\n- Música\n- Idiomas\n- Arte y manualidades",
    "deportes": "Tenemos equipos de fútbol y baloncesto, además de clases de educación física",
    
    // Contacto
    "telefono": "Puede contactar con el colegio en el teléfono: 977 123 456",
    "email": "El email del colegio es: info@rosamolas.edu",
    "direccion": "Nos encontramos en: Calle Principal, 123",
    
    // Uniforme
    "uniforme": "El uniforme consiste en:\n- Polo blanco\n- Pantalón/falda azul marino\n- Jersey azul marino con el escudo del colegio",
    
    // Por defecto
    "default": "Soy el asistente virtual del Colegio Rosa Molas. ¿En qué puedo ayudarte?"
};

function findBestResponse(query) {
    query = query.toLowerCase();
    
    // Buscar coincidencias exactas primero
    for (let key in responses) {
        if (query.includes(key)) {
            return responses[key];
        }
    }
    
    // Si no hay coincidencias, devolver respuesta por defecto
    return responses["default"];
}

function speakText(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'es-ES';
    window.speechSynthesis.speak(utterance);
}
