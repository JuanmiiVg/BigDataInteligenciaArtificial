import gradio as gr
from gradio import ChatMessage
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def stream_with_thinking(user_message: str, history: list):
    """
    Muestra el RESUMEN del razonamiento interno del modelo.
    """
    thinking_content = ""
    response_content = ""
    has_yielded = False

    # Generar respuesta con thinking activado
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=user_message,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                include_thoughts=True,  # Habilita resúmenes
                thinking_budget=-1  # Thinking dinámico
            )
        )
    ):
        if not chunk.candidates:
            continue

        for part in chunk.candidates[0].content.parts:
            if not part.text:
                continue

            if part.thought:
                # Es thinking (RESUMEN)
                thinking_content += part.text
                has_yielded = True

                yield [
                    ChatMessage(
                        role="assistant",
                        content=thinking_content,
                        metadata={"title": "🧠 Razonamiento del modelo"}
                    ),
                    response_content if response_content else "..."
                ]
            else:
                # Es respuesta
                response_content += part.text
                has_yielded = True

                if thinking_content:
                    yield [
                        ChatMessage(
                            role="assistant",
                            content=thinking_content,
                            metadata={"title": "🧠 Razonamiento del modelo"}
                        ),
                        response_content
                    ]
                else:
                    yield response_content

    if not has_yielded:
        yield "Lo siento, no pude generar una respuesta."

demo = gr.ChatInterface(
    fn=stream_with_thinking,
    type="messages",
    title="🧠 Gemini 2.5 Flash Thinking",
    description="Modelo con razonamiento interno. **Nota:** El thinking que ves es un resumen.",
    examples=[
        "Si tengo 5 manzanas y compro el triple, ¿cuántas tengo?",
        "Explica el teorema de Pitágoras paso a paso"
    ]
)

demo.launch()