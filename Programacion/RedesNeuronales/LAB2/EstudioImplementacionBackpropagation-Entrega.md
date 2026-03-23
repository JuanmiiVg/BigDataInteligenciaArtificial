# 📄 Entrega — Laboratorio 2

## Análisis de Implementación de Backpropagation

### UD4 — Fundamentos de Deep Learning

---

## 👤 Datos del alumno/a

* Nombre: Juan Manuel Vega
* Grupo: 2526-BDA
* Fecha: 17 de febrero de 2026
* Versión analizada:

  * ☑️ Implementación orientada a objetos
  * ☑️ Implementación funcional
  * ☑️ Ambas

---

# 1️⃣ Objetivo del laboratorio

Este laboratorio tiene como objetivo:

* Analizar una implementación real de backpropagation.
* Identificar las partes fundamentales del algoritmo.
* Relacionar el código con los conceptos teóricos estudiados.
* Comprender cómo se calculan y aplican los gradientes.

---

# 2️⃣ Identificación estructural del código

## 2.1 Forward Pass

Indica:

* ¿Dónde se calcula la salida de la red?
* ¿Qué funciones intervienen?
* ¿Cómo se almacenan los valores intermedios?

Explicación:

**Implementación Funcional (backpropagationRNAscratch.py):**
- **Cálculo de salida**: Función `forward_propagate(network, row)` (líneas 90-99)
- **Funciones que intervienen**: 
  - `activate(weights, inputs)`: Calcula la suma ponderada + bias
  - `transfer(activation)`: Aplica función sigmoid (1.0 / (1.0 + exp(-activation)))
- **Almacenamiento**: Los valores se guardan en `neuron['output']` para cada neurona

**Implementación Orientada a Objetos (backPropScratch.py):**
- **Cálculo de salida**: Método `feedforward()` (líneas 13-15)
- **Funciones que intervienen**: 
  - `sigmoid(x)`: Función de activación (1 / (1 + np.exp(-x)))
  - `np.dot()`: Producto matricial para los pesos
- **Almacenamiento**: Valores en `self.layer1` (capa oculta) y `self.output` (capa de salida)

```python
# Funcional
def forward_propagate(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)  # Almacena aquí
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs

# OOP
def feedforward(self):
    self.layer1 = sigmoid(np.dot(self.input, self.weights1))  # Capa oculta
    self.output = sigmoid(np.dot(self.layer1, self.weights2))  # Salida final
```

---

## 2.2 Cálculo de la pérdida

* ¿Dónde se define la función de pérdida?
* ¿Qué tipo de pérdida se utiliza?
* ¿Cómo se calcula el error respecto al valor real?

Explicación:

**Implementación Funcional:**
- **Definición**: En `backward_propagate_error()` líneas 108-109
- **Tipo de pérdida**: Error cuadrático medio (MSE) implícito
- **Cálculo del error**: Diferencia directa entre salida y valor esperado
- **Codificación**: Usa one-hot encoding para las clases (líneas 130-131)

**Implementación OOP:**
- **Definición**: En método `backprop()` línea 18
- **Tipo de pérdida**: Error cuadrático medio (MSE)
- **Cálculo del error**: `(self.y - self.output)` - diferencia entre target y predicción

```python
# Funcional - Cálculo de error en capa de salida
else:
    for j in range(len(layer)):
        neuron = layer[j]
        errors.append(neuron['output'] - expected[j])  # Error directo

# Funcional - One-hot encoding
expected = [0 for i in range(n_outputs)]
expected[row[-1]] = 1  # Solo la clase correcta = 1

# OOP - Cálculo de gradientes con MSE
d_weights2 = np.dot(self.layer1.T,
   (2*(self.y - self.output) * sigmoid_derivative(self.output)))
```

**Diferencia clave**: La funcional usa clasificación multiclase con one-hot, la OOP parece diseñada para regresión o clasificación binaria.

---

## 2.3 Backward Pass

Identifica:

* ¿Dónde comienza el proceso de retropropagación?
* ¿Cómo se calculan los gradientes?
* ¿Se aplica explícitamente la regla de la cadena?

Describe el flujo hacia atrás:

**Implementación Funcional:**
- **Inicio**: Función `backward_propagate_error(network, expected)` línea 105
- **Dirección**: Desde la última capa hacia la primera `for i in reversed(range(len(network)))`
- **Cálculo de gradientes**: 
  - Capa de salida: `error = neuron['output'] - expected[j]`
  - Capas ocultas: `error += (neuron['weights'][j] * neuron['delta'])` - propaga el error
- **Regla de la cadena**: Í`neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])`

**Implementación OOP:**
- **Inicio**: Método `backprop()` línea 17
- **Cálculo de gradientes**: Directamente con matrices NumPy
- **Regla de la cadena**: Explícita en ambas capas:
  - `d_weights2`: Error * derivada de sigmoid en capa de salida
  - `d_weights1`: Propagación del error a través de weights2 * derivada de capa oculta

```python
# Funcional - Flujo hacia atrás
def backward_propagate_error(network, expected):
    for i in reversed(range(len(network))):  # Última → primera capa
        layer = network[i]
        errors = list()
        if i != len(network)-1:  # Capas ocultas
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:  # Suma errores de capa siguiente
                    error += (neuron['weights'][j] * neuron['delta'])
                errors.append(error)
        else:  # Capa de salida
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(neuron['output'] - expected[j])
        
        # Aplicar regla de la cadena
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])

# OOP - Regla de la cadena explícita
def backprop(self):
    # ∂L/∂w2 = layer1^T * (∂L/∂output * ∂output/∂z2)
    d_weights2 = np.dot(self.layer1.T,
       (2*(self.y - self.output) * sigmoid_derivative(self.output)))
    
    # ∂L/∂w1 = input^T * (∂L/∂layer1 * ∂layer1/∂z1)
    d_weights1 = np.dot(self.input.T,
      (np.dot(2*(self.y - self.output) * sigmoid_derivative(self.output),
      self.weights2.T) * sigmoid_derivative(self.layer1)))
```

**Flujo**: Error de salida → Gradientes capa salida → Propagación a capa oculta → Gradientes capa oculta

---

## 2.4 Actualización de pesos

* ¿Dónde se actualizan los parámetros?
* ¿Qué fórmula se utiliza?
* ¿Existe tasa de aprendizaje configurable?

Explicación:

**Implementación Funcional:**
- **Ubicación**: Función `update_weights(network, row, l_rate)` líneas 118-125
- **Fórmula**: `w = w - η * δ * x` (gradiente descendente clásico)
- **Tasa de aprendizaje**: Sí, parámetro `l_rate` configurable (0.03 por defecto)
- **Proceso**: Actualiza peso por peso, neurona por neurona, capa por capa

**Implementación OOP:**
- **Ubicación**: Al final del método `backprop()` líneas 23-24
- **Fórmula**: `w = w + η * ∇w` (suma directa de gradientes)
- **Tasa de aprendizaje**: No explícita (implícita en el cálculo del gradiente)
- **Proceso**: Actualización matricial directa

```python
# Funcional - Actualización tradicional
def update_weights(network, row, l_rate):
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                # w_ij = w_ij - η * δ_i * x_j
                neuron['weights'][j] -= l_rate * neuron['delta'] * inputs[j]
            # Bias update
            neuron['weights'][-1] -= l_rate * neuron['delta']

# OOP - Actualización matricial
def backprop(self):
    # ... cálculo de gradientes ...
    self.weights1 += d_weights1  # ¡NOTA: Debería ser -= !
    self.weights2 += d_weights2  # ¡NOTA: Debería ser -= !
```

**Diferencias importantes**:
1. **Funcional**: Implementa correctamente w = w - η∇w
2. **OOP**: Tiene error conceptual (usa + en lugar de -), pero funciona porque los gradientes ya incluyen el signo
3. **Funcional**: Tasa de aprendizaje explícita y configurable
4. **OOP**: Tasa de aprendizaje implícita en el factor "2" del gradiente

---

# 3️⃣ Relación entre código y teoría

Completa la siguiente tabla:

| Concepto teórico       | Fragmento de código | Explicación |
| ---------------------- | ------------------- | ----------- |
| Forward pass | **Funcional:** `activation = activate(neuron['weights'], inputs)`<br>**OOP:** `self.layer1 = sigmoid(np.dot(self.input, self.weights1))` | Calcula la suma ponderada (w·x + b) y aplica la función de activación. El funcional lo hace neurona por neurona, el OOP usa operaciones matriciales. |
| Función de pérdida | **Funcional:** `errors.append(neuron['output'] - expected[j])`<br>**OOP:** `2*(self.y - self.output)` | Calcula la diferencia entre predicción y valor real. El funcional usa one-hot encoding, el OOP usa MSE con factor 2 para simplificar la derivada. |
| Gradiente | **Funcional:** `neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])`<br>**OOP:** `d_weights1 = np.dot(self.input.T, (...))` | Representa ∂L/∂w. El funcional almacena δ (gradiente local), el OOP calcula directamente el gradiente completo usando la regla de la cadena. |
| Regla de la cadena | **Funcional:** `error += (neuron['weights'][j] * neuron['delta'])`<br>**OOP:** `np.dot(..., self.weights2.T) * sigmoid_derivative(self.layer1)` | Propaga el error desde capas posteriores. Multiplica gradiente local por pesos para obtener gradiente de la capa anterior: ∂L/∂x = ∂L/∂y · ∂y/∂x. |
| Actualización de pesos | **Funcional:** `neuron['weights'][j] -= l_rate * neuron['delta'] * inputs[j]`<br>**OOP:** `self.weights1 += d_weights1` | Aplica gradiente descendente: w_nuevo = w_viejo - η∇w. El funcional es explícito, el OOP usa += porque los gradientes ya incluyen la dirección correcta. |

---

# 4️⃣ Análisis comparativo (si se analizan ambas versiones)

Si has analizado ambas implementaciones:

* ¿Cuál es más clara estructuralmente?
* ¿Cuál facilita mejor la comprensión del algoritmo?
* ¿Cuál sería más escalable a redes más profundas?
* ¿Qué diferencias observas en organización del código?

Conclución comparativa:

**Claridad estructural:**
La **implementación funcional** es más clara porque separa cada etapa del algoritmo en funciones independientes (`forward_propagate`, `backward_propagate_error`, `update_weights`). Cada función tiene una responsabilidad única y es fácil de seguir.

**Facilita comprensión del algoritmo:**
La **funcional** es superior para aprender porque:
- Muestra paso a paso cada cálculo (neurona por neurona)
- Los bucles for hacen explícito el flujo de datos
- Se puede "debuggear" fácilmente cada neurona
- Corresponde directamente a la explicación teórica tradicional

La **OOP** es más concisa pero "oculta" los detalles en operaciones matriciales.

**Escalabilidad a redes profundas:**
La **implementación OOP** es más escalable porque:
- Operaciones matriciales (NumPy) son mucho más eficientes
- Fácil extensión a múltiples capas 
- Aprovecha optimizaciones de hardware (GPU, BLAS)
- Menos bucles anidados = mejor rendimiento

La funcional se vuelve prohibitivamente lenta con muchas neuronas.

**Organización del código:**

| Aspecto | Funcional | OOP |
|---------|-----------|-----|
| **Modularidad** | Excelente (funciones separadas) | Buena (métodos de clase) |
| **Legibilidad** | Alta (paso a paso) | Media (compacta) |
| **Mantenimiento** | Fácil de modificar etapas | Cambios requieren conocer matrices |
| **Reutilización** | Funciones independientes | Encapsulación en clase |
| **Eficiencia** | Baja (bucles Python) | Alta (vectorización NumPy) |

**Conclusión final:**
- **Para aprender**: Funcional (transparencia didáctica)
- **Para producción**: OOP (eficiencia y escalabilidad)
- **Enfoque híbrido**: Usar funcional para entender, OOP para implementar

---

# 5️⃣ Análisis conceptual

Responde de forma argumentada:

1. **¿Backpropagation es el algoritmo de aprendizaje? Justifica.**

No, backpropagation **no es** el algoritmo de aprendizaje completo. Es únicamente el método para **calcular gradientes** de manera eficiente en redes neuronales multicapa. El algoritmo de aprendizaje real es el **gradiente descendente** (o sus variantes como SGD, Adam, etc.), que usa los gradientes calculados por backpropagation para actualizar los pesos. 

Backpropagation resuelve el problema de "cómo calcular ∂L/∂w para cada peso", mientras que gradiente descendente resuelve "cómo usar esos gradientes para mejorar el modelo".

2. **¿Qué papel juega la función de activación en el cálculo de gradientes?**

La función de activación es **crucial** porque:
- Su **derivada** determina cuánto "fluye" el gradiente hacia atrás
- En el código vemos: `transfer_derivative(neuron['output'])` y `sigmoid_derivative(self.layer1)`
- Sin funciones de activación no lineales, la red sería solo una regresión lineal
- La derivada actúa como "amplificador" o "atenuador" del error que se propaga

3. **¿Qué ocurriría si la derivada de la activación fuese cero?**

Se produciría el **problema del gradiente evanescente**:
- El gradiente se "cortaría" en esa neurona: `neuron['delta'] = errors[j] * 0 = 0`
- Las capas anteriores no recibirían señal de error
- Esos pesos **dejarían de aprender** (gradiente = 0 → sin actualización)
- La red se "saturaría" y el entrenamiento se detendría efectivamente
- Ejemplo: sigmoid en los extremos (salida ≈ 0 o ≈ 1) tiene derivada ≈ 0

4. **¿Qué relación tiene el código analizado con lo que hace internamente PyTorch o TensorFlow?**

Este código implementa **exactamente los mismos principios** que PyTorch/TensorFlow, pero:

**Similitudes:**
- Mismo flujo: forward → loss → backward → update
- Misma matemática: regla de la cadena para gradientes
- Misma estructura: capas, pesos, funciones de activación

**Diferencias:**
- **Automatización**: PyTorch/TF calculan gradientes automáticamente (autograd)
- **Optimización**: Usan C++/CUDA, no Python puro
- **Escalabilidad**: Soportan GPU, paralelización, redes muy profundas
- **Flexibilidad**: Arquitecturas dinámicas, cualquier función diferenciable

En esencia, **estos frameworks hacen lo mismo pero de forma más sofisticada y eficiente**.

5. **¿Qué limitaciones tendría esta implementación para redes profundas?**

**Limitaciones importantes:**
- **Gradiente evanescente**: Con muchas capas, los gradientes se vuelven exponencialmente pequeños
- **Eficiencia**: Bucles Python son 100x-1000x más lentos que operaciones vectorizadas
- **Memoria**: Almacenar salidas de todas las neuronas no escala
- **Funciones de activación**: Sigmoid causa saturación; necesitaría ReLU, Batch Norm, etc.
- **Flexibilidad**: Código rígido para arquitecturas específicas
- **Inicialización**: Pesos aleatorios uniformes no funcionan bien en redes profundas
- **Regularización**: Sin dropout, batch norm, o técnicas modernas contra sobreajuste

Para superar estas limitaciones se necesitan: mejores funciones de activación, inicialización inteligente, normalización, conexiones residuales, y optimizadores adaptativos.

---

# 6️⃣ Reflexión final

Explica con tus palabras:

> ¿Cómo calcula realmente una red neuronal qué pesos debe modificar?

Una red neuronal "aprende" siguiendo un proceso muy elegante basado en **responsabilidad compartida**:

1. **Hace una predicción** (forward pass): Cada neurona contribuye con su "voto" ponderado por sus conexiones

2. **Mide su error total**: Compara la predicción final con la respuesta correcta

3. **Distribuye la culpa hacia atrás** (backward pass): 
   - La neurona de salida se "culpa" directamente por el error
   - Cada neurona de capas anteriores se culpa **proporcionalmente** a cuánto contribuyó al error de las neuronas siguientes
   - Es como un juego de "telefono roto" al revés: el mensaje de error viaja desde el final hacia el inicio

4. **Calcula cuánto cambiar cada peso**:
   - Si un peso "empujó" la respuesta en dirección correcta → se refuerza (aumento)
   - Si un peso "empujó" hacia dirección incorrecta → se debilita (disminución)
   - La magnitud del cambio depende de:
     - Cuánto error hay
     - Cuánto "contribuyó" ese peso específico
     - La tasa de aprendizaje (que tan rápido queremos cambiar)

**La magia está en la regla de la cadena**: permite calcular exactamente cuánto cada peso individual (de potencialmente millones) contribuyó al error final, y por tanto, cuánto debe cambiar.

Es como si cada peso fuera un "empleado" en una empresa, y el algoritmo calculara exactamente cuánto cada empleado contribuyó al éxito o fracaso del proyecto final, permitiendo bonificaciones y correcciones justas y precisas.

---

# 7️⃣ Resultados de Aprendizaje implicados

Este laboratorio contribuye a la evaluación de:

### RA1

* Comprende los fundamentos matemáticos del aprendizaje automático.
* Interpreta el cálculo de gradientes.

### RA2

* Analiza implementaciones de modelos.
* Relaciona teoría y práctica.
* Identifica componentes de un algoritmo de IA.

---

# 8️⃣ Autoevaluación

Valora del 1 al 5 tu nivel de comprensión:

* Entiendo cómo funciona el forward pass: **5/5** - Comprendo perfectamente cómo se calculan las salidas capa por capa, tanto en la implementación funcional (neurona por neurona) como en la OOP (operaciones matriciales)

* Entiendo cómo se calcula el gradiente: **5/5** - Puedo identificar claramente dónde y cómo se calculan los gradientes en ambas implementaciones, y entiendo que representan ∂L/∂w

* Entiendo cómo se aplica la regla de la cadena: **4/5** - Comprendo el concepto y puedo ver su aplicación en el código, especialmente en la propagación del error hacia atrás, aunque aún me cuesta la parte matemática más profunda

* Entiendo cómo se actualizan los pesos: **5/5** - Está muy claro en ambas implementaciones: gradiente descendente w = w - η∇w, y puedo identificar las diferencias entre la actualización escalar (funcional) y matricial (OOP)

---
