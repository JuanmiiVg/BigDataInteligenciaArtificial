import logging

# Configurar logging ANTES de otros imports
logging.basicConfig(level=logging.ERROR)
for logger_name in ['google', 'google.genai', 'google.genai.types']:
    logging.getLogger(logger_name).setLevel(logging.ERROR)

import asyncio
import os
import sys
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool import SseConnectionParams
from google.genai import types

# Cargar variables de entorno
load_dotenv()

# Tool personalizada: Calculadora
def calculate(expression: str) -> str:
    """Evalúa una expresión matemática simple.

    Args:
        expression: Expresión matemática como string (ej: "2 + 2", "10 * 5").

    Returns:
        El resultado de la evaluación.
    """
    try:
        # ADVERTENCIA: En producción, usar ast.literal_eval o similar
        result = eval(expression)
        return f"El resultado de {expression} es {result}"
    except Exception as e:
        return f"Error al evaluar: {str(e)}"

# URL del servidor MCP
MCP_SERVER_URL = "https://agents-mcp-hackathon-ipmentor.hf.space/gradio_api/mcp/sse"

async def create_multi_tool_agent():
    """Crea y ejecuta un agente con tools personalizadas y MCP"""

    # Verificar API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY no configurada")
        sys.exit(1)

    print("=" * 60)
    print("Ejemplo 5: Agente multi-tool (Custom + MCP + OpenRouter)")
    print("=" * 60)

    # Conectar a MCP
    print("\n🔌 Conectando al servidor MCP...")
    connection_params = SseConnectionParams(url=MCP_SERVER_URL)
    mcp_toolset = McpToolset(connection_params=connection_params)

    try:
        # Obtener tools MCP
        mcp_tools = await mcp_toolset.get_tools()

        # Combinar tools personalizadas + MCP
        all_tools = [calculate] + mcp_tools

        print(f"✅ Tools: 1 personalizada + {len(mcp_tools)} MCP")

        # Crear agente con OpenRouter
        agent = Agent(
            name="multi_tool_assistant",
            model=LiteLlm(
                model="openrouter/openai/gpt-4o-mini",
                api_key=api_key,
                api_base="https://openrouter.ai/api/v1"
            ),
            instruction="""Eres un asistente versátil especializado en:
            1. Cálculos matemáticos: Usa 'calculate' para operaciones
            2. Redes: Usa tools MCP para ejercicios de subnetting
            Elige la herramienta apropiada según la consulta.""",
            description="Asistente con calculadora y redes",
            tools=all_tools
        )

        print("✅ Agente creado con GPT-4o-mini")

        # Crear runner y sesión
        runner = Runner(
            app_name="multi_tool_app",
            agent=agent,
            session_service=InMemorySessionService()
        )

        session = await runner.session_service.create_session(
            app_name="multi_tool_app",
            user_id="user123"
        )

        # Ejecutar consultas mixtas
        queries = [
            "Calcula 23 * 47",
            "Dame un ejercicio simple de subnetting",
            "Si 3 routers cuestan 150€ y 5 switches 80€, ¿total?"
        ]

        for query in queries:
            print(f"\n{'='*60}")
            print(f"👤 Usuario: {query}")
            print("🤖 Agente: ", end="")

            content = types.Content(
                role='user',
                parts=[types.Part(text=query)]
            )

            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=content
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(part.text, end="", flush=True)

            print()

    finally:
        await mcp_toolset.close()
        print("\n✅ Conexión cerrada")

if __name__ == "__main__":
    asyncio.run(create_multi_tool_agent())