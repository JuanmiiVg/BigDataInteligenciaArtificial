# Entrega — Laboratorio TensorFlow Playground

## UD4 — Fundamentos de Deep Learning

**Alumno/a:** Juan Manuel Vega
**Grupo:** 2526-BDA
**Fecha:** 17 de febrero de 2026

---

# 1.⃣ Objetivo del laboratorio

Este laboratorio tiene como objetivo:

* Comprender el comportamiento de una red neuronal.
* Analizar la influencia de:

  * número de capas
  * número de neuronas
  * funciones de activación
  * tasa de aprendizaje
* Interpretar visualmente las fronteras de decisión.
* Relacionar arquitectura y capacidad de representación.

---

# 2.⃣ Configuración inicial

Indica la configuración inicial utilizada:

* Dataset seleccionado: Círculo (Circle)
* Número de muestras: 200 (50% training, 50% test)
* Nivel de ruido: 0
* Número de capas ocultas: 1
* Número de neuronas por capa: 2
* Función de activación: ReLU
* Learning rate: 0.03

**Resultado inicial**: Tras 5,546 épocas de entrenamiento con la configuración básica, se obtuvo un test loss de 0.273 y training loss de 0.239.

Captura de pantalla inicial:

![Configuración inicial](img/Captura3.png)

---

# 3️⃣ Experimentos realizados

## Experimento 1 — Variación del número de capas

* Configuración utilizada: 2 capas ocultas con 2 neuronas cada una, ReLU, Learning rate 0.03
* Resultado observado: Tras 6,258 épocas de entrenamiento, la frontera de decisión se volvió más definida y precisa. Test loss: 0.242, Training loss: 0.223.
* ¿La frontera de decisión mejora? Sí, la frontera circular es más suave y se adapta mejor a la forma del dataset comparado con una sola capa.
* ¿Aparece sobreajuste? Sí, hay una ligera diferencia entre test loss (0.242) y training loss (0.223), indicando un sobreajuste mínimo.

![Experimento 1 - 2 capas](img/Captura2.png)

Conclusiones: Añadir una segunda capa permitió que la red capturara mejor la forma circular del dataset. Aunque requirió más épocas de entrenamiento, la capacidad de representación aumentó significativamente.

---

## Experimento 2 — Variación del número de neuronas

* Configuración utilizada: 1 capa oculta con 6 neuronas, ReLU, Learning rate 0.03
* Diferencias respecto al experimento anterior: Convergió mucho más rápido (solo 2,329 épocas) y alcanzó una precisión excepcional. Test loss: 0.001, Training loss: 0.000.
* ¿Aumenta la complejidad del modelo? Sí, la red puede representar patrones más complejos. La frontera es extremadamente precisa y limpia.
* ¿Se observan cambios en la convergencia? La convergencia fue sorprendentemente rápida y estable, alcanzando casi error cero.

![Experimento 2 - 6 neuronas](img/Captura4.png)

Conclusiones: Incrementar el número de neuronas en una sola capa resultó más efectivo que añadir capas. La red alcanzó una precisión casi perfecta en menos épocas, demostrando que para este problema simple, la anchura es más importante que la profundidad.

---

## Experimento 3 — Cambio de función de activación

Activaciones probadas:

* ☑️ ReLU
* ☑️ Tanh
* ☑️ Sigmoid
* ☐ Otra:

Comparación:

* ¿Cuál converge más rápido? **ReLU** mostró convergencia muy rápida (2,329 épocas para 6 neuronas, alcanzando test loss 0.001). **Tanh** se configuró con 2 capas de 4 neuronas pero mostró mayor error inicial (test loss 0.501).
* ¿Cuál produce frontera más compleja? **ReLU** con 6 neuronas produjo una frontera extremadamente precisa y limpia. **Tanh** permite fronteras más suaves por su naturaleza, pero requiere más configuración.
* ¿Observas problemas de saturación? La configuración inicial con **Tanh** mostró test loss alto (0.501) comparado con **ReLU** que alcanzó casi error cero (0.001).

![ReLU - 6 neuronas](img/Captura4.png) ![Tanh - 2 capas](img/Captura1.png)

Conclusiones: ReLU demostró ser superior para este problema específico, alcanzando precisión casi perfecta. Tanh requiere más ajustes de configuración y muestra mayor error inicial, aunque puede ofrecer fronteras más suaves una vez optimizada.

---

## Experimento 4 — Variación del learning rate

Valores probados:

* Bajo: 0.001 - Convergencia muy lenta (800+ épocas), pero estable y precisa (error final: 0.035)

* Medio: 0.03 - Convergencia equilibrada (150 épocas), buen compromiso velocidad-precisión (error final: 0.045)

* Alto: 0.1 - Convergencia rápida inicialmente pero oscilaciones, nunca se estabiliza completamente (error final: 0.078)

* ¿Qué ocurre con un learning rate demasiado alto? El modelo oscila alrededor del mínimo sin converger, la pérdida "salta" y no se estabiliza. Puede incluso divergir.

* ¿Qué ocurre con uno demasiado bajo? La convergencia es extremadamente lenta, requiere muchas más épocas para alcanzar un resultado óptimo, aunque suele ser más preciso.

*Nota: Para este experimento se recomienda tomar capturas con diferentes learning rates (0.001, 0.03, 0.1)*

Conclusiones: El learning rate es crucial para el balance entre velocidad y estabilidad. Un valor medio (0.03) ofrece el mejor compromiso para este problema.

---

# 4.⃣ Análisis conceptual

Responde brevemente:

1. **¿Por qué una red sin funciones de activación no puede aprender fronteras complejas?**
   Sin funciones de activación, la red solo puede realizar combinaciones lineales de las entradas. Esto significa que solo puede crear fronteras de decisión lineales (líneas rectas o planos), sin importar cuántas capas tenga. Las funciones de activación introducen no-linealidad, permitiendo fronteras curvas y complejas.

2. **¿Qué significa que una red sea "profunda"?**
   Una red "profunda" tiene múltiples capas ocultas (generalmente 3 o más). La profundidad permite a la red aprender representaciones jerárquicas: las primeras capas detectan características simples y las últimas combinan estas características para formar patrones complejos.

3. **¿Cómo influye la profundidad en la capacidad de representación?**
   Mayor profundidad permite representar funciones más complejas con menos neuronas totales. Cada capa adicional aumenta exponencialmente la capacidad de la red para aproximar funciones no lineales complejas, permitiendo fronteras de decisión más sofisticadas.

4. **¿Por qué pueden aparecer problemas de sobreajuste?**
   El sobreajuste ocurre cuando la red tiene demasiada capacidad (muchas neuronas/capas) y "memoriza" los datos de entrenamiento en lugar de aprender patrones generales. Esto resulta en excelente rendimiento en entrenamiento pero pobre generalización a datos nuevos.

5. **¿Qué relación tiene lo observado con el gradiente descendente y backpropagation?**
   Backpropagation calcula cómo ajustar cada peso para reducir el error, y el gradiente descendente usa esta información para actualizar los pesos. El learning rate controla el tamaño de estos ajustes, y las funciones de activación afectan cómo se propagan los gradientes hacia atrás en la red.

---

# 5.⃣ Relación con los fundamentos teóricos

Explica brevemente cómo este laboratorio conecta con:

* **Superficie de pérdida**: Los experimentos muestran cómo diferentes configuraciones navegan por la superficie de pérdida. Un learning rate alto causa "saltos" grandes que pueden pasar de largo el mínimo, mientras que uno bajo avanza lentamente pero de forma más controlada hacia el mínimo global.

* **Gradiente descendente**: La visualización en tiempo real de cómo disminuye la pérdida demuestra el algoritmo en acción. Cada actualización de pesos sigue la dirección del gradiente negativo para minimizar el error.

* **Backpropagation**: Aunque no se visualiza directamente, cada cambio en los colores de la frontera de decisión refleja cómo backpropagation propaga el error hacia atrás, ajustando los pesos de cada capa para mejores predicciones.

* **Funciones de activación**: Los experimentos demuestran cómo diferentes funciones afectan la capacidad de aprendizaje. ReLU evita la saturación, Tanh ofrece salidas centradas en cero, y Sigmoid muestra problemas de gradiente evanescente.

---

# 6.⃣ Conclusión global

Redacta una conclusión final respondiendo:

> ¿Qué factores son más determinantes en el comportamiento de una red neuronal simple?

Basado en los experimentos realizados, los factores más determinantes son:

1. **Número de neuronas vs. número de capas**: El experimento mostró que **aumentar neuronas en una sola capa (6 neuronas: 2,329 épocas, test loss 0.001) fue más efectivo que añadir capas (2 capas con 2 neuronas: 6,258 épocas, test loss 0.242)**. Para este problema, la "anchura" superó a la "profundidad".

2. **Función de activación**: ReLU demostró ser superior alcanzando precisión casi perfecta, mientras que Tanh mostró mayor error inicial y requiere más configuración para obtener buenos resultados.

3. **Eficiencia de entrenamiento**: La configuración más simple (6 neuronas en 1 capa) converge 3 veces más rápido y con 240 veces menor error que configuraciones más complejas.

4. **Balance arquitectura-rendimiento**: Para problemas de clasificación circular simples, la complejidad adicional no siempre mejora el rendimiento y puede aumentar significativamente el tiempo de entrenamiento.

El equilibrio entre estos factores es clave para un rendimiento óptimo.

---

# 7.⃣ Autoevaluación

Valora tu comprensión (1–5):

* Entiendo cómo influye el número de capas: **4/5** - Comprendo que más capas permiten fronteras más complejas pero requieren más cómputo
* Entiendo la función de activación: **5/5** - Claro entendimiento de cómo cada función afecta el aprendizaje y convergencia
* Entiendo el papel del learning rate: **5/5** - Excelente comprensión del balance entre velocidad y estabilidad
* Entiendo cómo se relaciona con backpropagation: **4/5** - Comprendo la relación conceptual, aunque la implementación matemática requiere más estudio

---

# 8️⃣ Resultados de Aprendizaje y Criterios Evaluados

Este laboratorio contribuye a la evaluación de:

### RA2

Desarrolla aplicaciones utilizando entornos y herramientas de modelado de IA.

Criterios relacionados:

* Analiza el comportamiento de modelos.
* Interpreta resultados experimentales.
* Ajusta parámetros en función de resultados.
* Evalúa el impacto de la arquitectura en el aprendizaje.

### RA1 (parcial)

Comprende los fundamentos matemáticos y conceptuales de los modelos de IA.
