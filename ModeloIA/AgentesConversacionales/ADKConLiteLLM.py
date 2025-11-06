from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv

load_dotenv()

# Agente con OpenRouter
agent = Agent(
    name="deepseek_agent",
    model=LiteLlm(
        model="openrouter/deepseek/deepseek-r1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        api_base="https://openrouter.ai/api/v1"
    ),
    instruction="Eres un asistente que piensa paso a paso. Muestra tu razonamiento completo.",
    description="Agente con razonamiento usando DeepSeek R1"
)

print("✅ Agente con OpenRouter creado")