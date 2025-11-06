import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Chat con instrucciones de CoT
chat = client.chats.create(
    model='gemini-2.5-flash',
    config={
        'system_instruction': '''Piensa paso a paso.
        Muestra tu razonamiento entre [THINKING] y [/THINKING].
        Luego da tu respuesta final.'''
    }
)

response = chat.send_message("Si tengo 5 manzanas y compro el triple, ¿cuántas tengo?")
print(response.text)