# Laboratorio 4 — Apache Zeppelin: Spark interactivo

## UD3 · Análisis interactivo sobre Big Data

En este laboratorio vamos a trabajar con **Apache Zeppelin** como entorno de notebooks **nativo de Spark**, similar a Jupyter, pero orientado a **Big Data real**.

Zeppelin **no sustituye** a Spark ni a los scripts anteriores:
nos permite **explorar, analizar y visualizar datos** ya procesados con Spark.

---

## 1. Objetivos del laboratorio

Al finalizar este laboratorio deberías ser capaz de:

* Comprender qué es Apache Zeppelin y para qué se usa.
* Levantar Zeppelin conectado a un Spark Master existente.
* Ejecutar código Spark de forma interactiva.
* Leer datos en formato Parquet.
* Realizar consultas y visualizaciones básicas.
* Entender la diferencia entre:

  * *Spark por scripts*
  * *Spark interactivo*

---

## 2. Qué es Apache Zeppelin (muy breve)

Apache Zeppelin es:

* Un **entorno de notebooks** (como Jupyter)
* Diseñado para trabajar **directamente con Spark**
* Con soporte para:

  * PySpark
  * Spark SQL
  * Visualizaciones integradas

👉 Zeppelin trabaja **sobre el clúster Spark**, no aparte.

---

## 3. Requisitos previos

Debes tener funcionando:

* Spark Master activo (`spark-master`)
* Al menos un Worker (Plan A o B)
* Datos en Parquet generados en el **Lab 3**

Ruta esperada:

```
data/parquet/ventas/
```

---


## 4. Arranque de Zeppelin con Docker

### 4.1 Fichero `docker-compose.zeppelin.yml`

Crea este fichero en la carpeta del laboratorio (`Spark4`) con el siguiente contenido:

```yaml
services:
  zeppelin:
    image: apache/zeppelin:0.11.1
    container_name: zeppelin
    environment:
      ZEPPELIN_LOG_DIR: /logs
      ZEPPELIN_NOTEBOOK_DIR: /notebook
      MASTER: spark://spark-master:7077
      SPARK_MASTER: spark://spark-master:7077
    ports:
      - "8082:8080"
    volumes:
      - ./data:/opt/spark-data
    restart: unless-stopped
```

Notas:

- El contenedor usa el Zeppelin oficial `apache/zeppelin:0.11.1`.
- Espera un `Spark Master` accesible en `spark://spark-master:7077` en la misma red Docker (o adapta la URL).
- Monta `./data` del directorio del laboratorio en `/opt/spark-data` dentro del contenedor, de donde leerás los Parquet.

---

### 4.2 Arrancar Zeppelin con Docker Compose

Desde la carpeta `Spark4` ejecuta:

```bash
docker compose -f docker-compose.zeppelin.yml up -d
```

Abre el navegador en:

```
http://localhost:8082
```

Si tienes Docker Desktop en Windows, asegúrate de que la red permita resolver `spark-master` o conecta Zeppelin a la misma red donde esté corriendo tu Spark (o reemplaza `MASTER`/`SPARK_MASTER` por la dirección IP/host apropiado).

Si necesitas parar y borrar el contenedor:

```bash
docker compose -f docker-compose.zeppelin.yml down
```

---

⚠️ Recuerda: Zeppelin con Docker se usa como entorno interactivo; los jobs productivos deben ejecutarse como scripts en tu clúster Spark.
---

Con estos pasos tendrás Zeppelin ejecutándose localmente y conectado a tu `Spark Master`. Sigue después con la sección 5 para crear el notebook.

---

## 5. Crear el primer notebook

1. Pulsa **“Create new note”**
2. Nombre:

   ```
   UD3_Zeppelin_Exploracion
   ```
3. Intérprete: **pyspark**

---

## 6. Primeras celdas (muy guiadas)

### 6.1 Comprobar SparkSession

Ejecuta en una celda:

```python
spark
```

Debes ver información de la SparkSession activa.

👉 Esto confirma que Zeppelin **está conectado al clúster**.

---

### 6.2 Leer datos Parquet

```python
df = spark.read.parquet("/opt/spark-data/parquet/ventas")
df.printSchema()
```

---

### 6.3 Vista rápida de los datos

```python
df.show(10)
```

---

### 6.4 Filtro simple

```python
df.filter(df.importe > 100).show(10)
```

---

### 6.5 Agregación por ciudad

```python
res = (
    df.groupBy("ciudad")
      .count()
      .orderBy("count", ascending=False)
)

res.show()
```

---

## 7. Visualización básica en Zeppelin

1. Ejecuta la celda anterior.
2. Cambia la vista de **Table** a **Bar Chart**.
3. Usa:

   * `ciudad` → eje X
   * `count` → eje Y

👉 Sin código extra.
👉 Visualización **sobre Spark**, no sobre pandas.

---

## 8. Spark SQL en Zeppelin (muy potente)

### 8.1 Crear vista temporal

```python
df.createOrReplaceTempView("ventas")
```

---

### 8.2 Consulta SQL

```sql
%sql
SELECT ciudad, COUNT(*) AS num_ventas, SUM(importe) AS total
FROM ventas
GROUP BY ciudad
ORDER BY total DESC
```

Prueba también la visualización desde Zeppelin.

---

## 9. Qué aporta Zeppelin frente a scripts

Reflexiona (no contestes aún, será para la entrega):

* feedback inmediato
* exploración rápida
* menos fricción para análisis
* mismo motor Spark

👉 Zeppelin **no reemplaza** los jobs productivos.

---

## 10. Buenas prácticas (mensaje importante)

En entornos reales:

* Scripts Spark:

  * pipelines
  * procesos periódicos
* Zeppelin:

  * exploración
  * validación
  * análisis
  * prototipos

👉 Ambos conviven.

---

## 11. Evidencias mínimas

Para la entrega deberás incluir:

* Captura del notebook Zeppelin
* Una celda con:

  * lectura Parquet
  * agregación
* Una visualización creada desde Zeppelin

---

## 12. Lo que viene después

Con Zeppelin ya puedes:

* Entender mejor los datos
* Preparar visualizaciones
* Pasar a:

  * Kibana
  * Airflow
  * dashboards

👉 **Este laboratorio cierra el ciclo de procesamiento en la UD3**.

---

### Nota final

> Zeppelin no es “otro Jupyter”.
> Es una forma de trabajar **directamente sobre Big Data**.
