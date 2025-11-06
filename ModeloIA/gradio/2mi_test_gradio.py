import numpy as np
import gradio as gr

def sepia(input_img):
    """Aplica filtro sepia a una imagen"""
    # Matriz de transformación sepia
    sepia_filter = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])

    # Aplicar filtro
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()  # Normalizar

    return sepia_img

# Crear interfaz
demo = gr.Interface(
    fn=sepia,
    inputs=gr.Image(),    # Componente de carga de imagen
    outputs="image"       # Salida de imagen
)

demo.launch()