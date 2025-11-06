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
    name="assistant",
    model="gemini-2.5-flash",
    instruction="Eres un asistente útil y amigable. Responde de forma clara y concisa.",
    description="Asistente general que responde preguntas."
)

# Crear runner
runner = Runner(
    app_name="my_app",
    agent=agent,
    session_service=InMemorySessionService()
)

# Ejecutar consultas
async def main():
    # Crear sesión una sola vez (mantiene contexto conversacional)
    session = await runner.session_service.create_session(
        app_name="my_app",
        user_id="user123"
    )

    # Primera pregunta
    content1 = types.Content(
        role='user',
        parts=[types.Part(text="¿Qué es Python?")]
    )

    print("\n👤 Usuario: ¿Qué es Python?")
    print("🤖 Agente: ", end="")

    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content1
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end="", flush=True)

    print("\n")

    # Segunda pregunta (usa la misma sesión)
    content2 = types.Content(
        role='user',
        parts=[types.Part(text="Dame 3 ventajas de Python")]
    )

    print("👤 Usuario: Dame 3 ventajas de Python")
    print("🤖 Agente: ", end="")

    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content2
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end="", flush=True)

    print("\n")

# Ejecutar
asyncio.run(main())