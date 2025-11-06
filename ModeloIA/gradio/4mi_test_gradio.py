import os
from dotenv import load_dotenv
from google import genai

# Cargar configuración
load_dotenv()

# Crear cliente
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Crear chat
chat = client.chats.create(model='gemini-2.5-flash')

# Enviar mensaje
response = chat.send_message("Hola, ¿cómo estás?")
print(response.text)

# Continuar la conversación
response = chat.send_message("¿Qué puedes hacer?")
print(response.text)