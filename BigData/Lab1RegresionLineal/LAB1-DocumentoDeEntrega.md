# Documento de entrega - LAB1
Regresión con Spark MLlib (dataset en memoria)

## Información del estudiante

Nombre y apellidos:

Grupo:

Fecha de entrega:

---

# Objetivo del laboratorio

El objetivo de este laboratorio es comprender el funcionamiento básico de Spark MLlib entrenando un modelo de regresión sobre un dataset sencillo creado en código.

Se trabajará con:

- creación de dataset
- preparación de features
- entrenamiento del modelo
- generación de predicciones
- evaluación del modelo

---

# Archivos a entregar

Se deberá entregar un único archivo:

# Documento de entrega - LAB1
Regresión con Spark MLlib (dataset en memoria)

## Información del estudiante

Nombre y apellidos:

Grupo:

Fecha de entrega:

---

# Objetivo del laboratorio

El objetivo de este laboratorio es comprender el funcionamiento básico de Spark MLlib entrenando un modelo de regresión sobre un dataset sencillo creado en código.

Se trabajará con:

- creación de dataset
- preparación de features
- entrenamiento del modelo
- generación de predicciones
- evaluación del modelo

---

# Archivos a entregar

Se deberá entregar un único archivo:
# Documento de entrega - LAB1
Regresión con Spark MLlib (dataset en memoria)

## Información del estudiante

Nombre y apellidos:

Grupo:

Fecha de entrega:

---

# Objetivo del laboratorio

El objetivo de este laboratorio es comprender el funcionamiento básico de Spark MLlib entrenando un modelo de regresión sobre un dataset sencillo creado en código.

Se trabajará con:

- creación de dataset
- preparación de features
- entrenamiento del modelo
- generación de predicciones
- evaluación del modelo

---

# Archivos a entregar

Se deberá entregar un único archivo:

```text
lab1_spark_regresion.ipynb
```
o equivalente si usas zeppelin

El notebook debe ejecutarse completamente sin errores.

---

# Contenido mínimo del notebook

El notebook debe incluir las siguientes secciones.

## 1. Creación del dataset

Crear el dataset de viviendas utilizando `spark.createDataFrame`.

Mostrar el dataset utilizando:

```python
dataset.show()
```
---

## 2. Preparación de features

Crear la columna `features` utilizando `VectorAssembler`.

Mostrar el resultado con:

```python
dataset_features.select("features","price").show()
```
---
---

## 3. División del dataset

Dividir el dataset en entrenamiento y prueba utilizando:
```python
randomSplit
```
Indicar el tamaño aproximado de cada conjunto.

---

## 4. Entrenamiento del modelo

Entrenar un modelo de regresión utilizando:
```python
LinearRegression
```
---

## 5. Predicciones

Generar predicciones utilizando:
```python
model.transform()
```

Mostrar las columnas:

- features
- price
- prediction


---

## 6. Evaluación del modelo

Calcular la métrica RMSE utilizando `RegressionEvaluator`.

Mostrar el valor obtenido.

---

# Preguntas de reflexión

Responder brevemente en el notebook:

1. ¿Qué variables se utilizan como features?
2. ¿Cuál es la variable objetivo del modelo?
3. ¿Qué función cumple `VectorAssembler`?
4. ¿Por qué es necesario dividir el dataset en entrenamiento y prueba?
5. ¿Qué representa la métrica RMSE?

---

# Criterios de evaluación

| Criterio | Puntos |
|--------|-------|
| Creación correcta del dataset | 2 |
| Preparación correcta de features | 2 |
| Entrenamiento del modelo | 2 |
| Predicciones y visualización | 2 |
| Evaluación y explicación | 2 |

Puntuación total: 10 puntos