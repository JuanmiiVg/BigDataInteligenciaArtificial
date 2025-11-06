import asyncio
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

# Crear agente con OpenRouter
agent = Agent(
    name="deepseek_reasoning",
    model=LiteLlm(
        model="openrouter/deepseek/deepseek-r1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        api_base="https://openrouter.ai/api/v1"
    ),
    instruction="Piensa paso a paso y muestra tu razonamiento completo.",
    description="Agente con razonamiento DeepSeek R1"
)

# Ejecutar
runner = Runner(
    app_name="ejemplo",
    agent=agent,
    session_service=InMemorySessionService()
)

async def test_reasoning():
    print("🧠 Probando razonamiento con DeepSeek R1\n")

    # Crear sesión
    session = await runner.session_service.create_session(
        app_name="ejemplo",
        user_id="user1"
    )

    content = types.Content(
        role='user',
        parts=[types.Part(text="Si tengo 5 manzanas y compro el triple, ¿cuántas tengo?")]
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

asyncio.run(test_reasoning())