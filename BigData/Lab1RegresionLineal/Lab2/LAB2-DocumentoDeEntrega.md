# Documento de entrega - LAB2
Regresión con Spark MLlib utilizando dataset real

## Información del estudiante

Nombre y apellidos:

Grupo:

Fecha de entrega:

---

# Objetivo del laboratorio

El objetivo de este laboratorio es entrenar un modelo de regresión utilizando Spark MLlib sobre un dataset cargado desde fichero.

Se trabajará con:

- carga de datos desde CSV
- exploración del dataset
- preparación de features
- entrenamiento del modelo
- evaluación del modelo

---

# Archivos a entregar

Se deberán entregar los siguientes archivos:

```

lab2_spark_housing.ipynb
housing_spark.csv

```

El notebook debe ejecutarse completamente sin errores.

---

# Contenido mínimo del notebook

El notebook debe incluir las siguientes secciones.

---

## 1. Carga del dataset

Cargar el archivo:

```

housing_spark.csv

```

utilizando:

```

spark.read.csv

```

Mostrar:

```

dataset.show()
dataset.printSchema()

```

---

## 2. Exploración del dataset

Mostrar:

- primeras filas del dataset
- tipos de columnas
- número total de registros

---

## 3. Preparación de features

Crear la columna `features` utilizando `VectorAssembler`.

Variables utilizadas:

```

size
bedrooms
age

```

Variable objetivo:

```

price

```

---

## 4. División del dataset

Dividir el dataset en entrenamiento y prueba utilizando:

```

randomSplit

```

---

## 5. Entrenamiento del modelo

Entrenar un modelo utilizando:

```

LinearRegression

```

---

## 6. Predicciones

Aplicar el modelo sobre el conjunto de prueba utilizando:

```

transform()

```

Mostrar las columnas:

```

features
price
prediction

```

---

## 7. Evaluación

Calcular la métrica RMSE utilizando:

```

RegressionEvaluator

```

Mostrar el resultado.

---

# Preguntas de reflexión

Responder brevemente:

1. ¿Qué variables se utilizan como features?
2. ¿Cuál es la variable objetivo?
3. ¿Por qué es necesario crear la columna `features`?
4. ¿Qué diferencia hay entre `fit()` y `transform()`?
5. ¿Qué indica la métrica RMSE?

---

# Criterios de evaluación

| Criterio | Puntos |
|--------|-------|
| Carga correcta del dataset | 2 |
| Preparación de features | 2 |
| Entrenamiento del modelo | 2 |
| Predicciones correctas | 2 |
| Evaluación y explicación | 2 |

Puntuación total: 10 puntos
