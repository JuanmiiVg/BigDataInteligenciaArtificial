import gradio as gr
from datetime import datetime

def get_current_time(message, history):
    """Retorna la hora actual en formato amigable"""
    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p")
    return f"La hora actual es {current_time}."

# Crear interfaz de chat
demo = gr.ChatInterface(
    fn=get_current_time,
    type="messages",  # Formato moderno compatible con APIs de LLMs
    title="Time Bot",
    description="Bot que te dice la hora actual"
)

demo.launch()