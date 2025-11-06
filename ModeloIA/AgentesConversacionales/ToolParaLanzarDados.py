import logging

# ⚠️ IMPORTANTE: Configurar logging ANTES de cualquier otro import
# para suprimir warnings internos de google.genai
logging.basicConfig(level=logging.ERROR)
for logger_name in ['google', 'google.genai', 'google.genai.types']:
    logging.getLogger(logger_name).setLevel(logging.ERROR)

import asyncio
import random
import os
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.genai import types

# Cargar configuración
load_dotenv()

def roll_die(sides: int, tool_context: ToolContext) -> int:
    """Lanza un dado y devuelve el resultado.

    Args:
        sides: El número de caras del dado (entero positivo).

    Returns:
        Un entero con el resultado de lanzar el dado.
    """
    result = random.randint(1, sides)

    # Guardar en el estado del agente
    if 'rolls' not in tool_context.state:
        tool_context.state['rolls'] = []
    tool_context.state['rolls'].append(result)

    print(f"   🎲 Resultado del dado: {result}")
    return result

def check_prime(nums: list[int]) -> str:
    """Verifica si los números dados son primos.

    Args:
        nums: Lista de números a verificar.

    Returns:
        Un string indicando qué números son primos.
    """
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    primes = [n for n in nums if is_prime(n)]

    if primes:
        return f"{', '.join(map(str, primes))} son números primos."
    else:
        return "No se encontraron números primos."

# Crear agente con tools personalizadas
dice_agent = Agent(
    name="dice_agent",
    model="gemini-2.5-flash",
    instruction="""Lanzas dados y verificas números primos.
    Cuando te pidan lanzar dados:
    1. Primero llama a roll_die con el número de caras
    2. Luego llama a check_prime con el resultado
    3. Explica el resultado al usuario de forma amigable""",
    description="Agente que lanza dados y verifica primos",
    tools=[roll_die, check_prime]
)

runner = Runner(
    app_name="ejemplo3",
    agent=dice_agent,
    session_service=InMemorySessionService()
)

async def play_dice():
    print("=" * 60)
    print("Ejemplo 3: Agente con tools personalizadas")
    print("=" * 60)
    print("\n🎲 Lanzando dados y verificando primos\n")

    # Crear sesión
    session = await runner.session_service.create_session(
        app_name="ejemplo3",
        user_id="user1"
    )

    print("👤 Usuario: Lanza un dado de 20 caras y dime si el resultado es primo")
    print("🤖 Agente: ", end="")

    content = types.Content(
        role='user',
        parts=[types.Part(text="Lanza un dado de 20 caras y dime si el resultado es primo")]
    )

    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content
    ):
        # 1. Detectar y mostrar llamadas a herramientas
        function_calls = event.get_function_calls()
        if function_calls:
            for func_call in function_calls:
                print(f"\n   🔧 [LLAMADA A TOOL] {func_call.name}(", end="")
                args_str = ", ".join([f"{k}={v}" for k, v in func_call.args.items()])
                print(f"{args_str})")

        # 2. Detectar y mostrar respuestas de herramientas
        function_responses = event.get_function_responses()
        if function_responses:
            for func_resp in function_responses:
                result = func_resp.response.get('result', func_resp.response)
                print(f"   ✅ [RESULTADO] → {result}")

        # 3. Mostrar respuesta final del modelo (solo texto)
        if event.is_final_response():
            # Iterar parts manualmente para extraer solo texto
            if event.content and event.content.parts:
                text_parts = []
                for part in event.content.parts:
                    # Solo procesar parts que sean texto puro (sin function_call)
                    if hasattr(part, 'text') and part.text:
                        # Verificar que NO sea un function_call part
                        if not (hasattr(part, 'function_call') and part.function_call is not None):
                            text_parts.append(part.text)

                if text_parts:
                    final_text = "".join(text_parts)
                    print(f"\n💬 [RESPUESTA FINAL]\n{final_text}")

    print("\n\n" + "=" * 60)
    print("Segundo intento:")
    print("=" * 60)
    print("\n👤 Usuario: Lanza 3 dados de 10 caras y dime cuáles son primos")
    print("🤖 Agente: ", end="")

    content2 = types.Content(
        role='user',
        parts=[types.Part(text="Lanza 3 dados de 10 caras y dime cuáles son primos")]
    )

    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content2
    ):
        # 1. Detectar y mostrar llamadas a herramientas
        function_calls = event.get_function_calls()
        if function_calls:
            for func_call in function_calls:
                print(f"\n   🔧 [LLAMADA A TOOL] {func_call.name}(", end="")
                args_str = ", ".join([f"{k}={v}" for k, v in func_call.args.items()])
                print(f"{args_str})")

        # 2. Detectar y mostrar respuestas de herramientas
        function_responses = event.get_function_responses()
        if function_responses:
            for func_resp in function_responses:
                result = func_resp.response.get('result', func_resp.response)
                print(f"   ✅ [RESULTADO] → {result}")

        # 3. Mostrar respuesta final del modelo (solo texto)
        if event.is_final_response():
            # Iterar parts manualmente para extraer solo texto
            if event.content and event.content.parts:
                text_parts = []
                for part in event.content.parts:
                    # Solo procesar parts que sean texto puro (sin function_call)
                    if hasattr(part, 'text') and part.text:
                        # Verificar que NO sea un function_call part
                        if not (hasattr(part, 'function_call') and part.function_call is not None):
                            text_parts.append(part.text)

                if text_parts:
                    final_text = "".join(text_parts)
                    print(f"\n💬 [RESPUESTA FINAL]\n{final_text}")

    print("\n\n✅ Pruebas completadas")

if __name__ == "__main__":
    asyncio.run(play_dice())