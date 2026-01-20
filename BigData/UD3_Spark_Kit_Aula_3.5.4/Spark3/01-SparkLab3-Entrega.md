# UD3 — Laboratorio 3: Spark, Parquet y particionado
## Documento de entrega del grupo

---

## 1. Datos del grupo

**Grupo :**  
**Fecha de entrega:**  

### Integrantes
- Alumno/a 1:
- Alumno/a 2:
- Alumno/a 3:

---

## 2. Objetivo del laboratorio

El objetivo de este laboratorio ha sido:

- Trabajar con **formatos de almacenamiento Big Data**.
- Transformar datos desde CSV a **Parquet** usando Spark.
- Aplicar **particionado** para mejorar el acceso a los datos.
- Comprender cómo influyen el formato y la organización en el rendimiento.
- Preparar los datos para su uso posterior (BI, análisis, pipelines).

---

## 3. Dataset utilizado

### Dataset de entrada
- Nombre:
- Formato:
- Número aproximado de filas:
- Tamaño aproximado:

### Dataset de salida
- Formato final:
- Ruta de salida:
- ¿Está particionado?: ☐ Sí ☐ No  
- Columna usada para particionar (si procede):

> …

---

## 4. Conversión a Parquet

### 4.1 Descripción del proceso

Explica brevemente cómo se ha realizado la conversión de CSV a Parquet con Spark:

- Lectura del dataset original
- Escritura en formato Parquet
- Número de ficheros generados (aproximado)

> …

---

### 4.2 Observaciones sobre Parquet

Describe qué has observado al trabajar con Parquet:

- estructura de carpetas
- tamaño de los ficheros
- diferencias frente a CSV

> …

---

## 5. Particionado de datos

### 5.1 Particionado aplicado

Indica si se ha aplicado particionado:

- ☐ No se ha particionado  
- ☐ Sí, se ha particionado por la columna: __________

Justifica brevemente la elección de esa columna:

> …

---

### 5.2 Estructura resultante

Describe (o esquematiza) la estructura generada tras el particionado:

Ejemplo:
```

parquet/ventas/
ciudad=Cadiz/
ciudad=Jerez/
ciudad=Algeciras/

```

> …

---

## 6. Lectura y uso del dataset Parquet

Indica qué operaciones se han realizado leyendo desde Parquet:

- ☐ Filtros
- ☐ Agrupaciones
- ☐ Consultas por una partición concreta
- ☐ Otras (indicar):

Describe brevemente alguna de estas operaciones:

> …

---

## 7. Preguntas de reflexión (obligatorias)

Responde de forma razonada a las siguientes cuestiones.

---

### 7.1 ¿Por qué CSV no es adecuado para Big Data?

> …

---

### 7.2 ¿Qué ventajas aporta Parquet frente a CSV?

Menciona al menos dos ventajas claras.

> …

---

### 7.3 ¿Qué problema resuelve el particionado?

Explícalo con un ejemplo práctico.

> …

---

### 7.4 ¿Cuándo NO tendría sentido particionar un dataset?

Piensa en volumen, cardinalidad de la columna o tipo de consultas.

> …

---

### 7.5 ¿Qué formato usarías como base de un datalake? ¿Por qué?

> …

---

## 8. Relación con los laboratorios anteriores

Explica brevemente cómo encaja este laboratorio con:

- **Lab 1 (Spark básico)**:
- **Lab 2 (pandas vs Spark)**:

> …

---

## 9. Evidencias de ejecución

Incluye al menos una de las siguientes evidencias:

- ☐ Captura de la estructura de carpetas Parquet
- ☐ Captura del `spark-submit`
- ☐ Fragmento del código usado para escribir Parquet
- ☐ Captura de una lectura desde Parquet

(Pega aquí las imágenes o enlázalas).

---

## 10. Problemas encontrados y soluciones

Describe cualquier problema técnico encontrado durante el laboratorio y cómo lo resolvisteis.

| Problema | Solución |
|--------|---------|
|        |          |
|        |          |

---

## 11. Conclusión del grupo

Redacta una conclusión conjunta (5–10 líneas) respondiendo a:

> ¿Qué has aprendido en este laboratorio sobre el almacenamiento y organización de datos en Big Data?

> …

---

## 12. Valoración del trabajo en grupo (opcional)

- Reparto de tareas:
- Coordinación:
- Qué mejoraríais en el siguiente bloque:

> …



