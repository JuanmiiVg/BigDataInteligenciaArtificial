---
output:
  pdf_document: 
    latex_engine: xelatex
    toc: true
  html_document: default
---

# PIA — Ejercicio Clasificacion ANN
## Clasificación con Redes Neuronales (ANN)  
### Predicción de Riesgo COVID-19 con MLP (PyTorch / Keras) o dataset similar


### 0. Datos del Alumno
Alumno o alumna(s):

- Nombre y apellidos:
- Nombre y apellidos (si procede):

Grupo:  
Fecha de entrega:

## 1. Contexto

En esta tarea desarrollarás un modelo de **clasificación binaria mediante una Red Neuronal Multicapa (MLP)** para predecir el riesgo de complicaciones graves por COVID-19 a partir de variables demográficas y clínicas.

Se evaluará el pipeline completo de Machine Learning:

- Preprocesamiento
- Modelado
- Entrenamiento
- Evaluación
- Regularización
- Visualización con TensorBoard
- Análisis crítico

---

## 2. Resultados de Aprendizaje Trabajados

- **RA1** — Selección y uso adecuado de lenguajes y librerías de IA.
- **RA2** — Desarrollo de aplicaciones de IA aplicando técnicas de modelado.


---

## 3. Estructura Obligatoria de Entrega

La entrega deberá contener la siguiente estructura:

```text

/proyecto_clasificacion_ann
|
|-- notebook.ipynb  (o script .py principal)
|-- README.md
|-- informe.pdf (o .md)
|-- results/
|   |-- tensorboard/
|   └-- graficas/
└-- requirements.txt (si procede)

```

---

## 4. Requisitos Técnicos

### 4.1 Dataset

Debe indicarse claramente:

- Fuente del dataset
- Variable objetivo
- Variables seleccionadas
- Justificación de selección

---

### 4.2 Preprocesamiento (Obligatorio)

Debe incluir:

- Limpieza de datos
- Tratamiento de valores nulos
- Codificación de variables categóricas
- Normalización o estandarización
- División 70% / 15% / 15%

Se deben justificar las decisiones adoptadas.

---

### 4.3 Arquitectura del Modelo

Requisitos mínimos:

- Red MLP
- 1–3 capas ocultas
- Activación ReLU en capas ocultas
- Activación Sigmoide en salida
- Función de pérdida: Binary Cross Entropy
- Optimizador: Adam o SGD

Debe mostrarse:

- Arquitectura final
- Número de parámetros
- Justificación técnica

---

### 4.4 Regularización

Debe probarse al menos una técnica:

- Dropout
- L2
- Batch Normalization

Debe compararse modelo con y sin regularización.

---

### 4.5 Métricas Obligatorias

En validación y test:

- Accuracy
- Recall (Sensibilidad)
- Specificity
- F1-score
- AUC-ROC
- Matriz de confusión

---

### 4.6 Comparativa

Debe entrenarse al menos un modelo clásico de referencia:

- Regresión logística  
o  
- Árbol de decisión  

Y compararse los resultados.

---

### 4.7 TensorBoard (Obligatorio)

Debe incluir capturas de:

- Evolución de la pérdida
- Evolución de accuracy
- Comparación entrenamiento vs validación
- Comparación de hiperparámetros (si procede)

---

## 5. Informe Técnico

Debe responder a:

1. ¿Qué variables seleccionaste y por qué?
2. ¿Cómo diseñaste la arquitectura?
3. ¿Existe sobreajuste o subajuste?
4. ¿Cómo afectó la regularización?
5. ¿Qué hiperparámetro tuvo mayor impacto?
6. ¿Qué mejorarías?

Debe incluir análisis crítico, no solo descripción.

---

## 6. Criterios de Evaluación

| Criterio | Peso |
|----------|------|
| Preprocesamiento correcto | 15% |
| Arquitectura coherente | 15% |
| Implementación técnica | 20% |
| Evaluación rigurosa | 15% |
| Uso de TensorBoard | 10% |
| Comparativa con modelo clásico | 10% |
| Análisis crítico | 10% |
| Claridad y documentación | 5% |

---

# RÚBRICA DETALLADA

## Nivel Excelente (9–10)

- Pipeline completo y bien estructurado.
- Justificación técnica sólida.
- Comparativa clara entre modelos.
- Uso adecuado de regularización.
- Análisis explícito de sobreajuste / subajuste.
- Visualizaciones completas en TensorBoard.
- Discusión crítica profunda.

## Nivel Notable (7–8)

- Implementación correcta.
- Métricas bien calculadas.
- Justificación aceptable.
- Uso básico de regularización.
- Análisis correcto pero no profundo.

## Nivel Aprobado (5–6)

- Modelo funcional.
- Métricas mínimas correctas.
- Preprocesamiento básico.
- Justificación limitada.
- Sin análisis profundo.

## Insuficiente (<5)

- División incorrecta de datos.
- Métricas mal calculadas.
- Falta de justificación.
- No uso de TensorBoard.
- Implementación incompleta o incorrecta.

---

## Penalizaciones

- No separar validación.
- No justificar decisiones.
- Métricas incorrectas.
- Código desorganizado.
- Entrega fuera de formato.

---


