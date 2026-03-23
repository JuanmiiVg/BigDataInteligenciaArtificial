# Laboratorio 1 — Primer contacto con Spark
## Procesamiento distribuido sobre datos ya integrados

---

## 0. Objetivo del laboratorio
[link text](00-SparkLab1-Preparacion.md)
El objetivo de este laboratorio **no es aprender Spark en profundidad**, sino:

- Ver cómo se trabaja con datos usando Spark.
- Comparar el enfoque con pandas.
- Entender qué aporta Spark cuando el volumen crece.
- Ejecutar un flujo completo de lectura → transformación → agregación.

Partimos de **datos ya preparados**:
- Integrados
- Anonimizados
- Con calidad aplicada

---

## 1. Punto de partida

Disponemos de un dataset final procedente de la UD2, por ejemplo:

- `ventas_clientes_anon.csv`
- o un dataset equivalente (ventas + turismo, etc.)

Este dataset contiene columnas como:

- fecha
- ciudad
- canal
- importe
- unidades
- identificador anónimo (`id_hash`)

👉 **No vamos a limpiar ni integrar datos aquí**.
Eso ya está hecho.

---

## 2. ¿Por qué usar Spark aquí?

Antes de empezar, idea clave:

> Vamos a hacer **operaciones que ya sabemos hacer con pandas**,
> pero usando un motor preparado para escalar.

No buscamos todavía grandes volúmenes reales, sino **el cambio de modelo mental**.

---

## 3. Arranque del entorno Spark

### 3.1 Contexto de trabajo

Según el entorno disponible, se trabajará en uno de estos formatos:

- Spark en local (modo standalone).
- Notebook con PySpark.
- Zeppelin (si está disponible).

En todos los casos, **el código Spark es el mismo**.

---

### 3.2 Crear la sesión Spark

Toda aplicación Spark comienza creando una **SparkSession**.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("UD3-Lab1") \
    .getOrCreate()
````

Explicación docente:

* `SparkSession` es el punto de entrada a Spark.
* Gestiona:

  * recursos
  * ejecución
  * comunicación interna
* Es equivalente, conceptualmente, a “iniciar pandas”, pero a escala distribuida.

---

## 4. Cargar los datos con Spark

### 4.1 Lectura del dataset

```python
df = spark.read.csv(
    "ventas_clientes_anon.csv",
    header=True,
    inferSchema=True
)
```

Comparación con pandas:

```python
# pandas
pd.read_csv("ventas_clientes_anon.csv")
```

Ideas clave a remarcar:

* La sintaxis es distinta, pero la intención es la misma.
* Spark **no carga todo el dataset de golpe en memoria**.
* El esquema se puede inferir o definir explícitamente.

---

### 4.2 Inspección inicial de los datos

```python
df.printSchema()
```

```python
df.show(5)
```

Explicación:

* `printSchema()` muestra la estructura distribuida del DataFrame.
* `show()` devuelve una muestra, no todo el dataset.

👉 En Spark **no se inspecciona todo**, solo fragmentos.

---

## 5. Operaciones básicas (equivalentes a pandas)

### 5.1 Selección de columnas

```python
df.select("ciudad", "canal", "importe").show(5)
```

Paralelismo mental:

* pandas: `df[["ciudad", "canal", "importe"]]`
* Spark: `select(...)`

---

### 5.2 Filtrado de datos

Ejemplo: ventas con importe mayor de 100.

```python
df_filtrado = df.filter(df.importe > 100)
df_filtrado.show(5)
```

Idea clave:

* La operación **no se ejecuta inmediatamente**.
* Spark construye un **plan de ejecución**.

---

## 6. Agregaciones: donde Spark empieza a brillar

### 6.1 Agregación por ciudad

```python
from pyspark.sql.functions import sum, avg, count

ventas_ciudad = df.groupBy("ciudad").agg(
    count("*").alias("num_ventas"),
    sum("importe").alias("importe_total"),
    avg("importe").alias("importe_medio")
)

ventas_ciudad.show()
```

Comparación conceptual con pandas:

* pandas: `groupby().agg()`
* Spark: `groupBy().agg()`

Diferencia real:

* Spark reparte los datos por nodos.
* Las agregaciones se hacen **en paralelo**.

---

### 6.2 Agregación por canal y ciudad

```python
ventas_canal_ciudad = df.groupBy("ciudad", "canal").agg(
    sum("importe").alias("importe_total")
)

ventas_canal_ciudad.show()
```

Aquí es importante remarcar:

* Spark puede manejar muchas combinaciones.
* El coste crece mejor que en pandas cuando el volumen aumenta.

---

## 7. Comparación conceptual con pandas

Pausa didáctica (muy importante):

Preguntas para el alumnado:

* ¿Qué hemos hecho que no sepamos hacer con pandas?
* ¿Qué cambia realmente aquí?
* ¿Por qué Spark no es “mejor” siempre?

Conclusión esperada:

> Spark no es más potente por la sintaxis,
> sino por **cómo ejecuta** las operaciones.

---

## 8. Guardar resultados procesados

Una vez obtenidos los resultados agregados, los guardamos para:

* Visualización posterior (Kibana).
* Uso en otros procesos.

### 8.1 Guardar a CSV

```python
ventas_ciudad.write.csv(
    "output/ventas_por_ciudad",
    header=True,
    mode="overwrite"
)
```

Explicación:

* Spark escribe en **múltiples ficheros** (particiones).
* Esto es normal en Big Data.

👉 No es un error, es una característica.

---

## 9. Cierre del laboratorio

### 9.1 Qué hemos aprendido hoy

* A arrancar una sesión Spark.
* A leer datos con Spark.
* A realizar:

  * filtros
  * selecciones
  * agregaciones
* A entender la diferencia conceptual con pandas.

---

### 9.2 Qué NO hemos hecho (todavía)

* No hemos montado clústeres complejos.
* No hemos optimizado rendimiento.
* No hemos automatizado procesos.

Todo eso vendrá **después**.

---

## 10. Preparación para el siguiente paso

Los datos procesados en este laboratorio servirán para:

* Visualización con Kibana.
* Trabajo interactivo con Zeppelin.
* Orquestación con Airflow.

👉 Spark es el motor, no el final del camino.

---

## 11. Pregunta final para reflexión

> Si este dataset creciera 100 veces…, (puedes ejecutar el script para engoradar el dataset)
> ¿seguirías usando pandas?
