import os
from dotenv import load_dotenv
from google.adk.agents import Agent

# Cargar configuración
load_dotenv()

# Definir agente
agent = Agent(
    name="assistant",
    model="gemini-2.5-flash",
    instruction="Eres un asistente útil y amigable. Responde de forma clara y concisa.",
    description="Asistente general que responde preguntas."
)

print("✅ Agente creado correctamente")
print(f"   - Nombre: {agent.name}")
print(f"   - Modelo: {agent.model}")