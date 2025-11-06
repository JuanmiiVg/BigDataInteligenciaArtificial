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
from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool import SseConnectionParams
from google.genai import types

# Cargar variables de entorno
load_dotenv()

# URL del servidor MCP de IPMentor
MCP_SERVER_URL = "https://agents-mcp-hackathon-ipmentor.hf.space/gradio_api/mcp/sse"

async def run_mcp_demo():
    """Ejecuta una demo completa con el agente MCP"""

    # Verificar API key
    api_key = os.getenv("GOOGLE_GENAI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: Configura GOOGLE_GENAI_API_KEY o GOOGLE_API_KEY")
        sys.exit(1)

    os.environ["GOOGLE_GENAI_API_KEY"] = api_key

    print("🔌 Conectando al servidor MCP...")

    # Crear parámetros de conexión SSE
    connection_params = SseConnectionParams(url=MCP_SERVER_URL)

    # Crear toolset MCP - maneja la conexión automáticamente
    mcp_toolset = McpToolset(connection_params=connection_params)

    try:
        print("✅ Conexión establecida con IPMentor")

        # Obtener las tools del servidor MCP (es asíncrono)
        mcp_tools = await mcp_toolset.get_tools()
        print(f"✅ {len(mcp_tools)} herramientas MCP cargadas")

        # Crear agente con las tools MCP
        agent = Agent(
            name="network_teacher",
            model="gemini-2.5-flash",
            instruction="""Eres un profesor de redes y subnetting.
            Usa las herramientas MCP disponibles para generar ejercicios educativos,
            analizar redes y ayudar a los estudiantes a comprender el direccionamiento IP.
            Presenta la información de forma clara y estructurada.""",
            description="Agente educativo de redes usando MCP",
            tools=mcp_tools
        )

        print("✅ Agente MCP creado")

        # Crear runner
        runner = Runner(
            app_name="mcp_app",
            agent=agent,
            session_service=InMemorySessionService()
        )

        # Crear sesión
        session = await runner.session_service.create_session(
            app_name="mcp_app",
            user_id="user123"
        )

        # Ejecutar consulta de ejemplo
        query = "Dame un ejercicio de VLSM con subredes de diferentes tamaños"

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

        print("\n")

    finally:
        # Cerrar conexión MCP
        await mcp_toolset.close()
        print("✅ Conexión cerrada")

if __name__ == "__main__":
    asyncio.run(run_mcp_demo())