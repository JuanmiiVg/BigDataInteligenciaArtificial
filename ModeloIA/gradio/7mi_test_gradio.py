import gradio as gr
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Cliente OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def chat_openrouter(message, history, model):
    """Chat con modelo seleccionable"""
    # Convertir historial de Gradio a formato OpenAI
    messages = []
    if history:
        for msg in history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    # Añadir mensaje actual
    messages.append({"role": "user", "content": message})

    # Llamar a OpenRouter
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content

# Interfaz con selector de modelo
with gr.Blocks(theme=gr.themes.Ocean()) as demo:
    gr.Markdown("# 🌐 Chat con OpenRouter - Acceso a 100+ Modelos")

    with gr.Row():
        model_selector = gr.Dropdown(
            choices=[
                "openai/gpt-4",
                "openai/gpt-3.5-turbo",
                "anthropic/claude-3-opus",
                "anthropic/claude-3-sonnet",
                "meta-llama/llama-3-70b",
                "mistralai/mistral-large",
                "google/gemini-2.5-flash",
                "tngtech/deepseek-r1t2-chimera:free"  # Modelo con razonamiento completo
            ],
            value="openai/gpt-3.5-turbo",
            label="Selecciona el modelo",
            interactive=True
        )

    gr.Markdown("""
    **💡 Tip:** Prueba `tngtech/deepseek-r1t2-chimera:free` para ver un modelo que expone 
    **todo su razonamiento** entre etiquetas `<think>...</think>` (no solo un resumen como Gemini).
    """)

    chatbot = gr.ChatInterface(
        fn=lambda msg, hist: chat_openrouter(msg, hist, model_selector.value),
        type="messages",
        chatbot=gr.Chatbot(height=500),
        examples=[
            "Hola, ¿cómo estás?",
            "Explícame qué es la inteligencia artificial",
            "Si tengo 5 manzanas y compro el triple, ¿cuántas tengo?"  # Prueba con DeepSeek R1
        ]
    )

demo.launch()