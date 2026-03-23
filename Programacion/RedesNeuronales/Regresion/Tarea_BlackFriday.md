# Tarea: Black Friday Dataset con PyTorch y Keras

## Introducción

El conjunto de datos **Black Friday** es un dataset popular para analizar el comportamiento de compra de los clientes en retail. Contiene información sobre transacciones de compras realizadas por clientes en una tienda, incluyendo datos demográficos y categorías de productos.

Este dataset presenta un problema interesante para practicar tanto técnicas de **regresión** (predecir el monto de compra) como de **clasificación** (predecir la categoría de producto).

### Descripción del Dataset

El dataset contiene las siguientes columnas:

| Columna | Descripción |
|---------|-------------|
| User_ID | Identificador único del usuario |
| Product_ID | Identificador único del producto |
| Gender | Género del usuario (M/F) |
| Age | Edad del usuario |
| Occupation | Ocupación del usuario (categoría) |
| City_Category | Categoría de la ciudad (A, B, C) |
| Stay_In_Current_City_Years | Años de residencia en la ciudad actual |
| Marital_Status | Estado civil (0=soltero, 1=casado) |
| Product_Category_1 | Categoría principal del producto |
| Product_Category_2 | Categoría secundaria (opcional) |
| Product_Category_3 | Categoría terciaria (opcional) |
| Purchase | Monto de la compra (variable objetivo) |

---

## Objetivos de la Tarea

1. **Preprocesar datos**: Manejar variables categóricas, valores faltantes y normalizar datos.
2. **Implementar modelos**: Construir redes neuronales tanto en PyTorch como en Keras.
3. **Experimentar con técnicas**: Aplicar regularización, normalización por lotes y diferentes optimizadores.
4. **Comparar resultados**: Analizar el rendimiento de ambos frameworks y técnicas.

---

## Descripción de la Tarea

### Parte A: Preprocesamiento de Datos

1. **Carga y exploración del dataset**:
   - Carga los datos desde el archivo CSV proporcionado.
   - Analiza la distribución de las variables.
   - Identifica y maneja valores faltantes (Product_Category_2 y Product_Category_3 tienen valores nulos).
   - Analiza la variable objetivo (Purchase).

2. **Transformación de variables**:
   - Codifica las variables categóricas (Gender, Age, City_Category, Stay_In_Current_City_Years) usando técnicas apropiadas (Label Encoding, One-Hot Encoding, o embeddings).
   - Normaliza/estandariza las variables numéricas.
   - Decide si usar el dataset completo o un subconjunto para el entrenamiento (justifica tu decisión).

### Parte B: Modelo de Regresión con PyTorch

3. **Construye una red neuronal** en PyTorch para predecir el monto de compra:
   - Arquitectura: 3-4 capas ocultas con 64-128 neuronas cada una.
   - Funciones de activación: ReLU o ELU.
   - Regularización: Dropout y/o L2.

4. **Entrena el modelo**:
   - Usa el optimizador Adam.
   - Implementa early stopping.
   - Utiliza validación cruzada o un conjunto de validación.

5. **Evalúa el modelo**:
   - Calcula métricas: MSE, RMSE, MAE, R².
   - Grafica las curvas de entrenamiento y validación.

### Parte C: Modelo de Regresión con Keras

6. **Implementa el mismo modelo** en Keras:
   - Mantén una arquitectura similar para poder comparar.
   - Usa la API funcional o secuencial.

7. **Compara con PyTorch**:
   - ¿Obtienes resultados similares?
   - Analiza diferencias en tiempo de entrenamiento.

### Parte D: Mejoras y Experimentación

8. **Experimenta con diferentes configuraciones**:
   - Añade normalización por lotes (Batch Normalization).
   - Prueba diferentes funciones de activación (ReLU, ELU, SELU).
   - Experimenta con distintos optimizadores (Adam, SGD, RMSprop).
   - Ajusta hiperparámetros (learning rate, batch size, número de épocas).

9. **Análisis de resultados**:
   - ¿Cuál configuración obtuvo mejores resultados?
   - ¿El modelo está sobreajustando o subajustando?
   - ¿Cómo afectan las técnicas de regularización al rendimiento?

### Parte E (Opcional): Clasificación

10. **Extensión**: En lugar de predecir el monto de compra, puedes intentar predecir la categoría de producto principal (Product_Category_1) como un problema de clasificación multiclase.

### Parte F: Visualización con TensorBoard

11. **Configura TensorBoard** en tus modelos:
    - **En Keras**: Usa el callback `TensorBoard` con `histogram_freq=1` para registrar histogramas de pesos y sesgos.
    - **En PyTorch**: Usa `torch.utils.tensorboard.SummaryWriter`.

12. **Registra información durante el entrenamiento**:
    - Pérdida y métricas en entrenamiento y validación.
    - Histogramas de pesos y sesgos de cada capa.
    - Gradientes (opcional, puede ser muy detallado).

13. **Analiza las visualizaciones** y responde a las siguientes preguntas en tu informe:
    - ¿Cómo evolucionan los pesos durante el entrenamiento? ¿Se observan patrones significativos?
    - ¿Hay evidencia de saturación en alguna capa (valores muy grandes o muy pequeños)?
    - ¿Puedes identificar cuándo comienza el sobreajuste observando las curvas de pérdida?
    - ¿Los histogramas de entrenamiento y validación tienen distribuciones similares (indicador de buena generalización)?
    - ¿Qué información adicional proporciona TensorBoard que no se ve en las curvas simples de pérdida?

14. **Compara visualizaciones** entre diferentes configuraciones:
    - Compara el comportamiento de los pesos con y sin Batch Normalization.
    - Observa diferencias entre optimizadores (Adam vs SGD).
    - Analiza el efecto del learning rate en la estabilidad del entrenamiento.

**Comandos para ejecutar TensorBoard**:

```bash
# Para Keras
tensorboard --logdir=logs/fit

# Para PyTorch
tensorboard --logdir=runs
```

### Uso de TensorBoard en Google Colab

En Google Colab, puedes usar TensorBoard de las siguientes formas:

**Opción 1: magic command**
```python
%load_ext tensorboard
%tensorboard --logdir=logs/fit
```

**Opción 2: Visualizador de TensorBoard de Colab**
```python
%tensorboard --logdir=logs/fit
```

**Opción 3: Desde la barra lateral de Colab**
- Activa "TensorBoard" en el menú "Ver" → "TensorBoard"

**Nota**: Asegúrate de que los logs se guarden en una carpeta accesible y de no entrenar con demasiadas épocas si el entorno tiene memoria limitada.

---

## Entregables

### Código Fuente

- Notebook o scripts con el código completo y documentado.
- El código debe ser reproducible y ejecutable.

### Informe

Un documento (Markdown o PDF) que incluya:

- Descripción del preprocesamiento aplicado y justificaciones.
- Arquitectura de las redes neuronales utilizadas.
- Gráficos de curvas de entrenamiento y validación (puedes usar los de TensorBoard).
- **Capturas de pantalla de TensorBoard** mostrando:
  - Evolución de pérdida y métricas.
  - Histogramas de pesos y sesgos.
  - Comparaciones entre configuraciones.
- Tabla comparativa de resultados (diferentes configuraciones, PyTorch vs Keras).
- Análisis de sobreajuste/subajuste.
- Respuestas a las preguntas de la Parte F sobre interpretación de TensorBoard.
- Conclusiones y recomendaciones.

---

## Criterios de Evaluación

| Criterio | Ponderación |
|----------|-------------|
| Correcto preprocesamiento de datos | 15% |
| Implementación correcta de modelos en PyTorch y Keras | 20% |
| Experimentación con diferentes configuraciones | 15% |
| **Uso correcto de TensorBoard y análisis de visualizaciones** | **15%** |
| Calidad del análisis y comparativa | 20% |
| Organización y documentación del código | 15% |

---

## Notas

- El archivo con el dataset se encuentra en: `SAA/blkfri_train.csv`
- Se recomienda dividir el dataset en entrenamiento (80%) y test (20%).
- Para la validación, usa una división del conjunto de entrenamiento (ej: 80/20).
- Comenta tu código para facilitar la comprensión.
- Se valorará la originalidad en las experimentaciones y el análisis crítico de los resultados.
