# 📘 Introducción a NumPy

## 🧠 ¿Qué es NumPy?
**NumPy (Numerical Python)** es una biblioteca fundamental para la computación científica en Python.  
Proporciona estructuras de datos y funciones optimizadas para el **cálculo numérico eficiente**, especialmente con grandes cantidades de datos.

👉 Mientras que las **listas** de Python son flexibles pero lentas, **los arrays de NumPy** son homogéneos y están implementados en **C**, lo que los hace mucho más rápidos y eficientes.

---

## ⚙️ ¿Para qué se usa?
NumPy se usa principalmente para:

- 🧮 **Cálculos matemáticos y estadísticos** (sumas, medias, desviaciones, etc.).  
- 📊 **Procesamiento y análisis de datos numéricos**.  
- 🧠 **Entrenamiento de modelos de IA y Machine Learning** (bases de datos y tensores).  
- 🧬 **Ciencia e ingeniería**: simulaciones, álgebra lineal, transformadas, estadísticas.  
- 🧱 **Base de otras librerías**: casi todo el ecosistema de IA y Big Data se construye sobre NumPy.

---

## 🔗 Librerías que usan NumPy
NumPy es el **núcleo numérico** de muchas librerías modernas de ciencia de datos e IA:

| Categoría | Librerías basadas en NumPy |
|------------|----------------------------|
| Análisis de datos | `pandas`, `polars`, `xarray` |
| Machine Learning | `scikit-learn`, `TensorFlow`, `Keras`, `PyTorch` (interfaz NumPy-like) |
| Visualización | `matplotlib`, `seaborn`, `plotly` |
| Cálculo simbólico | `sympy` |
| Computación científica | `SciPy`, `OpenCV`, `scikit-image` |
| Aceleración GPU | `CuPy`, `JAX NumPy`, `RAPIDS/cuDF` |

---

## 🧩 Estructura básica: el array de NumPy
El objeto principal de NumPy es el **array multidimensional**, representado por la clase `ndarray`.

```python
import numpy as np

# Crear un array desde una lista
a = np.array([1, 2, 3, 4])
print(a)
print("Tipo:", type(a))
print("Dimensiones:", a.ndim)
print("Forma:", a.shape)
print("Tipo de datos:", a.dtype)
````

---

## 🧮 Operaciones básicas con arrays

NumPy permite realizar operaciones **vectorizadas**, sin bucles explícitos:

```python
b = np.array([10, 20, 30, 40])

print(a + b)   # Suma elemento a elemento
print(a * 2)   # Multiplicación escalar
print(a ** 2)  # Potencia
print(np.sqrt(a))  # Raíz cuadrada
```

---

## 🧠 Categorías principales de funciones en NumPy

| Categoría                  | Ejemplos de funciones                                            | Descripción                        |
| -------------------------- | ---------------------------------------------------------------- | ---------------------------------- |
| **Creación de arrays**     | `array`, `arange`, `linspace`, `zeros`, `ones`, `random.rand`    | Crear datos iniciales              |
| **Aritméticas**            | `add`, `subtract`, `multiply`, `divide`, `power`                 | Operaciones matemáticas básicas    |
| **Estadísticas**           | `mean`, `median`, `std`, `sum`, `min`, `max`, `argmax`           | Cálculos agregados                 |
| **Álgebra lineal**         | `dot`, `matmul`, `inv`, `eig`, `det`                             | Matrices, productos, determinantes |
| **Lógicas**                | `greater`, `less`, `equal`, `logical_and`, `where`               | Comparaciones y condiciones        |
| **Manipulación de arrays** | `reshape`, `concatenate`, `split`, `flatten`, `transpose`        | Cambiar forma o combinar datos     |
| **Aleatorios**             | `random.rand`, `random.randn`, `random.randint`, `random.choice` | Generación de datos aleatorios     |
| **Transformadas**          | `fft.fft`, `fft.ifft`                                            | Transformadas de Fourier           |
| **Entrada/Salida**         | `loadtxt`, `savetxt`, `save`, `load`                             | Guardar y leer datos               |

---

## 🔬 Ejemplo práctico

```python
import numpy as np

# Creamos un array 2D
m = np.array([[1, 2, 3],
              [4, 5, 6]])

print("Matriz:\n", m)

# Estadísticas
print("Media:", np.mean(m))
print("Desviación estándar:", np.std(m))
print("Máximo:", np.max(m))
print("Suma por filas:", np.sum(m, axis=1))

# Álgebra lineal
print("Transpuesta:\n", m.T)
print("Producto punto:", np.dot(m[0], m[1]))
```

---

## ⚡ Rendimiento

Una de las ventajas clave de NumPy es su **velocidad** frente a las estructuras estándar de Python.
La vectorización evita los bucles en Python y utiliza **rutinas en C** optimizadas.

```python
import time

x = list(range(10_000_000))
y = np.arange(10_000_000)

# Python puro
t0 = time.perf_counter()
[xi * 2 for xi in x]
print("Python:", time.perf_counter() - t0)

# NumPy
t0 = time.perf_counter()
y * 2
print("NumPy:", time.perf_counter() - t0)
```

> ⚙️ En la mayoría de casos, NumPy será **10 a 100 veces más rápido** que Python puro en operaciones numéricas.

---

## 📚 Conclusión

NumPy es la **columna vertebral del ecosistema científico de Python**.
Gracias a su potencia y simplicidad, permite manejar y procesar grandes volúmenes de datos de forma rápida y eficiente, siendo la base de bibliotecas como **pandas**, **scikit-learn**, **TensorFlow**, **PyTorch** y **JAX**.

A lo largo del módulo aprenderemos a combinar NumPy con otras herramientas para construir modelos de **Inteligencia Artificial y Big Data**.

