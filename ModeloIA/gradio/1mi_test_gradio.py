import gradio as gr

def greet(name, intensity):
    """Función que genera un saludo con intensidad"""
    return "Hello, " + name + "!" * int(intensity)

# Crear interfaz
demo = gr.Interface(
    fn=greet,                    # Función a ejecutar
    inputs=["text", "slider"],   # Tipos de entrada
    outputs=["text"],            # Tipos de salida
)

# Lanzar la aplicación
demo.launch()