---
output:
  pdf_document: 
    latex_engine: xelatex 
    toc: true
    toc_depth: 2
    number_sections: false
    fig_caption: true
  html_document: default
---
# 🧪 Laboratorio Puente — Del Playground al Código Real

## UD4 → Transición hacia UD5

---

## 🎯 Contexto

En un laboratorio anterior hemos trabajado con **TensorFlow Playground**, experimentando visualmente con:

* número de capas
* número de neuronas
* funciones de activación
* learning rate
* fronteras de decisión

Ahora el objetivo es responder a la pregunta:

> ¿Podemos reproducir esos comportamientos en código real usando **Keras** o **PyTorch**?

Este laboratorio conecta la intuición visual con la implementación práctica.

---

# 🎯 Objetivos

* Reproducir en código uno de los datasets de TensorFlow Playground.
* **Implementar** una red neuronal equivalente en **Keras** o **Pytorch**.
* Comparar comportamiento visual vs entrenamiento real.
* Analizar convergencia, métricas y frontera de decisión.
* Relacionar arquitectura y resultado.

---

# 📂 Material proporcionado

* Notebook: `tf-playground-datasets.ipynb`
* Dataset generadores:

  * círculos
  * espirales
  * XOR
  * blobs

---

# 📝 Trabajo a realizar

## 1️⃣ Selección del dataset

Escoge uno de los siguientes:

* ☐ Círculos
* ☐ Espiral
* ☐ XOR
* ☐ Otro (justificar)

Indica por qué lo has elegido.

---

## 2️⃣ Implementación del modelo

Utilizando:

* ☐ Keras
* ☐ PyTorch

Implementa una red con:

* al menos 2 capas ocultas
* activación no lineal
* salida adecuada (sigmoid o softmax)

Incluye:

* definición del modelo
* función de pérdida
* optimizador
* entrenamiento

---

## 3️⃣ Visualización

Debes generar:

* gráfica de pérdida vs epochs
* frontera de decisión en 2D

Explica:

* ¿La frontera se parece a la del Playground?
* ¿Necesitaste más neuronas?
* ¿Necesitaste más épocas?

---

## 4️⃣ Experimento de profundidad

Repite el entrenamiento:

* con 1 capa
* con 2 capas
* con 3 capas

Compara:

* convergencia
* complejidad de la frontera
* estabilidad

Conclusión:

---

## 5️⃣ Experimento de activaciones

Prueba al menos dos activaciones distintas:

* ReLU
* Tanh
* Sigmoid

Responde:

* ¿Hay diferencias en convergencia?
* ¿Alguna genera inestabilidad?
* ¿Qué ocurre con el gradiente?

---

## 6️⃣ Reflexión conceptual

Responde de forma argumentada:

1. ¿Por qué el Playground parece más “rápido” que el entrenamiento real?
2. ¿Qué diferencia hay entre experimentar visualmente y entrenar realmente?
3. ¿Qué hemos ganado al pasar a código?
4. ¿Qué limita estos modelos frente a imágenes reales?

---

# 📊 Resultados de Aprendizaje implicados

### RA2

Desarrolla aplicaciones utilizando entornos de modelado de IA.

* Implementa modelos en frameworks reales.
* Ajusta hiperparámetros.
* Evalúa comportamiento experimental.
* Interpreta resultados.

### RA1 (parcial)

Comprende los fundamentos matemáticos del aprendizaje automático.

* Relaciona arquitectura y comportamiento.
* Interpreta la influencia de la activación.
* Analiza el efecto de la profundidad.

---

# 🧠 Criterios de evaluación

| Nivel        | Indicadores                                                                        |
| ------------ | ---------------------------------------------------------------------------------- |
| Excelente    | Implementación correcta, visualización clara, análisis profundo, reflexión crítica |
| Notable      | Modelo funcional, comparación adecuada, conclusiones correctas                     |
| Aprobado     | Modelo funcional básico, análisis superficial                                      |
| Insuficiente | Modelo incorrecto o sin análisis                                                   |

---

# 🏁 Entrega

Debe incluir:

* Notebook ejecutable
* Gráficas
* Respuestas reflexivas
* Conclusiones finales

---

# 🚪 Función del laboratorio

Este laboratorio sirve como:

* transición entre redes simples y Deep Learning aplicado
* preparación para trabajar con datos más complejos
* base para la siguiente unidad: **CNN y visión por computador**
