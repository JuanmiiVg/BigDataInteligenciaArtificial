import asyncio
import os
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents import Agent
from google.genai import types

# Cargar configuración
load_dotenv()

# Definir agente
agent = Agent(
    name="asistente_simple",
    model="gemini-2.0-flash-exp",
    instruction="Eres un asistente útil y amigable.",
    description="Asistente conversacional básico"
)

# Crear runner
runner = Runner(
    app_name="ejemplo",
    agent=agent,
    session_service=InMemorySessionService()
)

# Ejecutar
async def quick_test():
    # Crear sesión
    session = await runner.session_service.create_session(
        app_name="ejemplo",
        user_id="user1"
    )

    content = types.Content(
        role='user',
        parts=[types.Part(text="Hola, ¿cómo estás?")]
    )

    print("👤 Usuario: Hola, ¿cómo estás?")
    print("🤖 Agente: ", end="")

    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end='', flush=True)

    print("\n")

asyncio.run(quick_test())