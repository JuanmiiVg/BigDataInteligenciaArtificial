from google.adk.agents import Agent
from google.adk.tools import google_search
import asyncio
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agente con herramienta de búsqueda
search_agent = Agent(
    name="web_researcher",
    model="gemini-2.5-flash",
    instruction="Eres un investigador web. Usa Google Search cuando necesites información actualizada.",
    description="Agente que busca información en la web",
    tools=[google_search]
)

# Ejecutar
runner = Runner(
    app_name="ejemplo",
    agent=search_agent,
    session_service=InMemorySessionService()
)

async def research():
    session = await runner.session_service.create_session(
        app_name="ejemplo",
        user_id="user1"
    )

    content = types.Content(
        role='user',
        parts=[types.Part(text="¿Cuál es la temperatura actual en Tokio?")]
    )

    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end='', flush=True)

asyncio.run(research())