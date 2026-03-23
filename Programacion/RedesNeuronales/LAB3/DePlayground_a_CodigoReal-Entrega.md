# 📄 Entrega — Laboratorio 3

## Playground → Implementación Real con Keras / PyTorch

### UD4 — Redes Neuronales y Backpropagation

---

## 👤 Datos del alumno/a

* Nombre: Juan Manuel Vega
* Grupo: [Tu grupo]
* Fecha: 23 de febrero de 2026
* Framework utilizado:

  * ☑️ Keras
  * ☐ PyTorch
  * ☐ Ambos

---

# 1️⃣ Objetivo del laboratorio

En este laboratorio se parte de una configuración experimentada en **TensorFlow Playground** y se implementa en código real utilizando un framework de Deep Learning.

El objetivo es:

* Comprender cómo se traduce una arquitectura visual a código.
* Analizar el comportamiento del entrenamiento.
* Interpretar resultados y métricas.
* Conectar teoría, visualización y práctica real.

---

# 2️⃣ Dataset utilizado

* Tipo de dataset: **ESPIRAL**

* Problema:

  * ☑️ Clasificación binaria
  * ☐ Clasificación multiclase

* Breve descripción del dataset: Dos espirales entrelazadas generadas sintéticamente, siendo uno de los problemas más desafiantes para clasificación no lineal. Requiere una red neuronal compleja para separar las clases.

* Número de muestras: **1000**

* Número de variables: **2** (coordenadas X, Y)

---

# 3️⃣ Arquitectura implementada

Describe la arquitectura final utilizada:

* Número de capas ocultas: **3 capas**
* Número de neuronas por capa: **8, 6, 4 neuronas** respectivamente
* Funciones de activación: **ReLU** (capas ocultas), **Sigmoid** (salida)
* Función de pérdida: **binary_crossentropy**
* Optimizador: **Adam**
* Learning rate: **0.01**

Justifica brevemente las decisiones tomadas:

**Justificación:**
- **3 capas ocultas**: Los experimentos demostraron que más profundidad mejora significativamente la capacidad de representación para este problema complejo (68.5% vs 58% con 1 capa).
- **ReLU**: Demostró ser superior a Tanh y Sigmoid, evitando problemas de gradiente desvaneciente y proporcionando mejor convergencia.
- **Arquitectura decreciente (8→6→4)**: Permite una extracción jerárquica de características, de general a específico.
- **Adam optimizer**: Proporciona convergencia estable con learning rate adaptativo.

---

# 4️⃣ Experimentos realizados

Indica las configuraciones probadas (mínimo 2 variaciones):

| Experimento | Cambios realizados | Resultado obtenido | Observaciones |
| ----------- | ------------------ | ------------------ | ------------- |
| 1 Capa | 1 capa oculta (8 neuronas) + ReLU | 58% accuracy | Insuficiente para la complejidad del problema |
| 2 Capas | 2 capas ocultas (8, 4) + ReLU | 61.5% accuracy | Mejora notable pero aún limitada |
| 3 Capas | 3 capas ocultas (8, 6, 4) + ReLU | **68.5% accuracy** | **Mejor resultado** - Capacidad óptima |
| ReLU | 2 capas + activación ReLU | 60% accuracy | Convergencia rápida y estable |
| Tanh | 2 capas + activación Tanh | 57% accuracy | Convergencia más lenta |
| Sigmoid | 2 capas + activación Sigmoid | 51% accuracy | Problemas de gradiente desvaneciente |

---

# 5️⃣ Visualización del entrenamiento

Incluye y comenta:

* Curva de pérdida  ✅ **Implementada**
* Curva de accuracy (si aplica) ✅ **Implementada**  
* Frontera de decisión (si procede) ✅ **Implementada**

Explica:

* ¿Converge el modelo? 
**SÍ.** La pérdida decrece consistentemente de 0.68 a 0.60 durante 50 épocas, sin oscilaciones significativas.

* ¿Hay signos de sobreajuste?
**NO.** Las curvas de entrenamiento y validación siguen trayectorias similares, indicando generalización adecuada.

* ¿Se estabiliza la pérdida?
**SÍ.** Después de ~40 épocas la pérdida se estabiliza, sugiriendo convergencia efectiva.

* ¿Qué ocurre al aumentar profundidad o neuronas?
**Mejora sustancial:** 1 capa (58%) → 2 capas (61.5%) → 3 capas (68.5%). Más profundidad permite fronteras de decisión más complejas.

**Análisis:**
- La frontera de decisión muestra patrones curvos complejos, intentando separar las espirales entrelazadas
- El modelo captura parcialmente la estructura no lineal, pero el 68.5% indica la inherente dificultad del problema
- La visualización confirma que el modelo aprende patrones similares a los observados en TensorFlow Playground

---

# 6️⃣ Comparación con Playground

Responde:

1. **¿Los resultados obtenidos en código coinciden con lo observado en Playground?**

**Parcialmente SÍ.** Ambos muestran:
- Fronteras de decisión curvas y complejas
- Dificultad para separar completamente las espirales en el centro
- Mejora gradual con más capas y neuronas
- Patrones de aprendizaje similares durante el entrenamiento

2. **¿Qué diferencias encuentras?**

- **Precisión numérica:** Nuestro código proporciona métricas exactas (68.5% accuracy)
- **Control granular:** Podemos ajustar cada hiperparámetro específicamente  
- **Proceso completo:** Incluye normalización, validación y evaluación rigurosa
- **Complejidad visual:** Playground simplifica la visualización para didáctica

3. **¿Qué aporta el entorno real frente al visual?**

- **Escalabilidad:** Funciona con datasets de cualquier tamaño
- **Métricas profesionales:** Accuracy, loss, matrices de confusión
- **Reproducibilidad científica:** Resultados exactos y replicables
- **Flexibilidad total:** Cualquier arquitectura y configuración
- **Integración:** Compatible con pipelines de producción

4. **¿Qué limitaciones tiene Playground?**

- Datasets predefinidos y limitados
- Arquitecturas restringidas a configuraciones básicas
- Sin acceso a métricas detalladas de rendimiento
- Imposibilidad de guardar/cargar modelos entrenados
- Sin capacidad para problemas del mundo real

---

# 7️⃣ Conexión conceptual

Explica con tus palabras:

* **¿Dónde interviene el backpropagation en tu implementación?**

El backpropagation ocurre automáticamente durante cada época de entrenamiento cuando llamamos a `model.fit()`. TensorFlow calcula los gradientes de la función de pérdida respecto a cada peso, y los propaga hacia atrás capa por capa para ajustar los pesos usando el optimizador Adam. Este proceso se repite 50 veces (épocas) refinando progresivamente los parámetros.

* **¿Qué significa que el modelo "aprenda"?**

Aprender significa que la red ajusta iterativamente sus 65 parámetros (pesos y sesgos) para minimizar el error entre las predicciones y las etiquetas reales. Inicialmente los pesos son aleatorios, pero mediante backpropagation se modifican para reconocer patrones en los datos de espiral, mejorando gradualmente de ~50% a 68.5% accuracy.

* **¿Qué ocurre matemáticamente cuando la pérdida disminuye?**

Cuando la pérdida disminuye de 0.68 a 0.60, significa que la función de pérdida binaria (binary crossentropy) se acerca al mínimo global. Matemáticamente, los gradientes están conduciendo los pesos hacia valores que hacen que las predicciones del modelo se aproximen más a las etiquetas verdaderas, reduciendo la divergencia entre distribuciones.

* **¿Por qué puede fallar el entrenamiento?**

- **Learning rate inadecuado:** Muy alto causa oscilaciones, muy bajo causa convergencia lenta
- **Arquitectura insuficiente:** Pocas capas/neuronas limitan la capacidad de representación (como vimos con 1 capa)
- **Gradientes desvanecientes:** Con funciones como sigmoid (51% vs 60% con ReLU)
- **Datos inadequados:** Sin normalización o con ruido excesivo
- **Overfitting:** Con modelos muy complejos para pocos datos

---

# 8️⃣ Análisis técnico

Reflexiona:

* **¿Qué ocurre si el learning rate es demasiado alto?**

El modelo oscila alrededor del mínimo sin converger estable. Los gradientes son tan grandes que "saltan" de un lado a otro de la superficie de pérdida, impidiendo el refinamiento preciso de los pesos. En casos extremos, la pérdida puede incluso aumentar.

* **¿Qué ocurre si es demasiado bajo?**

La convergencia se vuelve extremadamente lenta. El modelo necesitaría cientos o miles de épocas para alcanzar el mismo nivel de rendimiento. En nuestro caso, con 0.01 obtuvimos buen balance entre velocidad y estabilidad.

* **¿Qué papel juega la función de activación?**

**CRÍTICO.** Nuestros experimentos lo demuestran claramente:
- **ReLU (60%):** Evita gradientes desvanecientes, permite flujo de información eficiente
- **Tanh (57%):** Introduce saturación en extremos, limitando el aprendizaje  
- **Sigmoid (51%):** Severos gradientes desvanecientes, prácticamente bloquea el aprendizaje

* **¿Cómo influye la profundidad de la red en la capacidad de representación?**

**Exponencialmente.** Cada capa adicional permite:
- **1 capa (58%):** Solo hiperplanos lineales con activación
- **2 capas (61.5%):** Combinaciones de hiperplanos, formas convexas básicas  
- **3 capas (68.5%):** Aproximación de funciones arbitrariamente complejas, curvatura sofisticada

La profundidad permite composición de funciones más complejas, esencial para separar espirales entrelazadas.

---

# 9️⃣ Conclusión final

Redacta una conclusión técnica:

* **Qué arquitectura ha funcionado mejor:** 

La configuración **3 capas ocultas (8, 6, 4 neuronas) + ReLU + Adam (lr=0.01)** alcanzó **68.5% accuracy**, siendo la mejor combinación probada. Esta arquitectura proporciona el balance óptimo entre capacidad representacional y estabilidad de entrenamiento.

* **Por qué:**

- **Profundidad suficiente:** 3 capas pueden aproximar la función compleja de separación de espirales
- **ReLU óptimo:** Evita gradientes desvanecientes manteniendo flujo de información
- **Arquitectura decreciente:** Extrae características jerárquicamente (general → específico)  
- **Hiperparámetros balanceados:** Learning rate permite convergencia estable en 50 épocas

* **Qué cambiarías si el dataset fuese más complejo:**

1. **Más neuronas:** 16, 32, 64 por capa para mayor capacidad
2. **Regularización:** Dropout (0.2-0.5) y L2 para prevenir overfitting
3. **Batch normalization:** Para acelerar convergencia y estabilidad
4. **Learning rate scheduling:** Reducción adaptativa durante entrenamiento
5. **Data augmentation:** Si aplicable, para aumentar robustez
6. **Ensemble methods:** Combinar múltiples modelos para mejor performance

* **Qué has aprendido sobre redes neuronales reales frente a visualizaciones:**

**Insight clave:** Playground proporciona intuición fundamental, pero el código real es donde la ciencia se convierte en ingeniería aplicable.

- **Control vs Simplicidad:** Código real da control total pero requiere comprensión profunda
- **Métricas vs Visualización:** Los números reales (68.5%) son más precisos que impresiones visuales
- **Escalabilidad vs Didáctica:** Playground enseña conceptos, código resuelve problemas reales
- **Complejidad emergente:** Los detalles técnicos (normalización, validación, optimización) son cruciales para éxito

La **transición exitosa de visual a código** requiere dominar tanto la intuición conceptual como la implementación técnica rigurosa.

---

# 🔟 Relación con Resultados de Aprendizaje

Este laboratorio evalúa:

### **RA1 - Fundamentos matemáticos del aprendizaje automático**

✅ **Demostrado:** 
- Relacioné arquitectura con comportamiento (profundidad → capacidad representacional)
- Interpreté influencia de activaciones (ReLU > Tanh > Sigmoid por gradientes)  
- Analicé efecto de profundidad en aproximación de funciones complejas
- Conecté backpropagation con ajuste de parámetros y minimización de pérdida

### **RA2 - Desarrollo de aplicaciones con entornos de modelado de IA**

✅ **Demostrado:**
- Implementé modelo completo con Keras/TensorFlow desde cero
- Ajusté sistemáticamente hiperparámetros (capas, activación, learning rate)
- Evalué comportamiento experimental con métricas cuantitativas  
- Interpreté resultados técnicamente y propuse mejoras fundamentadas
- Desarrollé pipeline completo: datos → modelo → entrenamiento → evaluación → visualización

---

## 🎯 **LABORATORIO 3 - COMPLETADO**
**Transición exitosa: TensorFlow Playground → Código Real con Keras**  
**Dataset: Espiral | Mejor resultado: 68.5% accuracy | Marco: Keras/TensorFlow 2.20.0**

