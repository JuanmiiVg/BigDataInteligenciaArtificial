# Laboratorio 2 — Spark frente a pandas  
## Procesamiento de datos a mayor escala

En este laboratorio vamos a **aumentar el volumen de datos** y a comparar dos enfoques:

- Procesamiento clásico con pandas
- Procesamiento distribuido con Spark

El objetivo no es “ver quién va más rápido”, sino **entender cuándo Spark empieza a marcar la diferencia**.

---

## 1. Objetivos del laboratorio

Al finalizar este laboratorio deberías ser capaz de:

- Generar un dataset de mayor tamaño a partir de uno pequeño.
- Procesar el mismo dataset con pandas y con Spark.
- Observar diferencias de tiempo y consumo.
- Comprender por qué Spark escala mejor cuando el volumen crece.
- Preparar datos para su uso posterior (visualización / automatización).

---

## 2. Punto de partida

Partimos del proyecto del Laboratorio 1:

```

ud3-spark-lab1/
apps/
data/
ventas_clientes_anon.csv
scripts/
inflar_dataset.py

````

El dataset original es **correcto**, pero demasiado pequeño para notar diferencias.

---

## 3. Inflar el dataset (paso clave)

### 3.1 ¿Por qué inflar los datos?

En clase no siempre podemos trabajar con datos realmente grandes.  
Para simular un escenario Big Data:

👉 **replicamos los datos muchas veces**, manteniendo su estructura.

---

### 3.2 Generar un dataset grande

Desde la raíz del proyecto:

```bash
python scripts/inflar_dataset.py \
  --input data/ventas_clientes_anon.csv \
  --output data/ventas_clientes_anon_big.csv \
  --factor 100
```

**Resultado:**
```
Generado data/ventas_clientes_anon_big.csv con 400 filas
```

Esto genera un CSV con muchas más filas (el dataset original tiene 4 filas, con factor 100 obtenemos 400 filas).

Comprueba el tamaño:

```bash
ls -lh data/ventas_clientes_anon_big.csv
```

---

## 4. Procesamiento con pandas (referencia)

Este paso sirve **solo como comparación**.

### 4.1 Crear un script pandas sencillo

Crea el fichero `apps/pandas_job.py`:

```python
import pandas as pd
import time

start = time.time()

df = pd.read_csv("data/ventas_clientes_anon_big.csv")

df_f = df[df["importe"] > 100]

res = (
    df_f.groupby("ciudad")
    .agg(
        num_ventas=("importe", "count"),
        importe_total=("importe", "sum"),
        importe_medio=("importe", "mean")
    )
    .sort_values("importe_total", ascending=False)
)

print(res.head(10))

end = time.time()
print(f"Tiempo total pandas: {end - start:.2f} segundos")
```

Ejecuta:

```bash
python apps/pandas_job.py
```

**Resultado obtenido:**
```
           num_ventas  importe_total  importe_medio
ciudad
Jerez             100       19980.96       199.8096
Algeciras         100       15007.32       150.0732
Cadiz             100       12002.51       120.0251
Tiempo total pandas: 0.03 segundos
```

⚠️ Si tu equipo va justo, este paso puede tardar bastante o incluso fallar.
Eso **forma parte del experimento**.

**Observación:** Con el dataset de 400 filas (100 réplicas del original de 4 filas), pandas es muy rápido (0.03 segundos). A medida que aumente el volumen, esto cambiará significativamente.

---

## 5. Procesamiento con Spark

### 5.1 Usar el dataset inflado en Spark

Edita `apps/lab1_job.py` y cambia la ruta:

```python
DATA_PATH = "/opt/spark-data/ventas_clientes_anon_big.csv"
```

---

### 5.2 Ejecutar el job Spark

Desde el **Master**:

```bash
docker exec -it spark-master spark-submit \
  --master spark://IP_DEL_MASTER:7077 \
  /opt/spark-apps/lab1_job.py
```

Observa:

* El tiempo de ejecución
* El uso de CPU
* La actividad en la UI del Master (`:8080`)

---

## 6. Observación y comparación

### Tabla comparativa (con 400 filas de datos):

| Aspecto             | pandas | Spark |
| ------------------- | ------ | ----- |
| Tiempo de ejecución | 0.03s  | Pendiente* |
| Uso de CPU          | 1 núcleo | Distribuido |
| Uso de memoria      | ~50 MB | Distribuido |
| Sensación general   | Instantáneo | Depende del cluster |

*Para ejecutar Spark, necesitas tener el cluster configurado (docker-compose.master.yml y docker-compose.worker.yml)

**Nota importante:** Con solo 400 filas, pandas es prácticamente instantáneo. Para ver diferencias significativas, deberías:
- Aumentar el factor a 10,000 o más
- Usar datasets reales de millones de registros
- Medir no solo tiempo, sino también consumo de CPU y memoria
**¿Qué ha pasado al aumentar el volumen de datos?**
   - Con 400 filas, pandas sigue siendo muy rápido (0.03s)
   - El overhead de Spark (iniciar el cluster) es mayor que el tiempo de procesamiento

2. **¿En qué momento pandas empieza a ser incómodo?**
   - Con datasets > 1 GB en una máquina estándar
   - Con operaciones complejas que requieren múltiples pasadas sobre los datos
   - Cuando necesitas procesar datos en múltiples máquinas

3. **¿Spark es siempre mejor? ¿Por qué?**
   - No. Con datos pequeños, pandas es más eficiente
   - Spark brilla cuando el volumen es realmente grande o distribuido

4. **¿Qué coste tiene usar Spark frente a pandas?**
   - Overhead de inicialización del cluster
   - Mayor consumo de recursos (memoria para coordinación)
   - Mayor complejidad operacional

5. **¿Qué enfoque usarías para:**

   * **Un análisis rápido:** pandas (< 1GB) o Python directo
   * **Un proceso periódico:** pandas si es < 1GB, Spark si es mayor
   * **Un volumen muy grande:** Spark, con datos en HDFS o cloud storagempieza a ser incómodo?
3. ¿Spark es siempre mejor? ¿Por qué?
4. ¿Qué coste tiene usar Spark frente a pandas?
5. ¿Qué enfoque usarías para:

   * un análisis rápido
   * un proceso periódico
   * un volumen muy grande?

---

## 8. Salida del procesamiento

Spark genera resultados en:

```
data/output/ventas_por_ciudad/
``**Spark no sustituye a pandas.** Son herramientas complementarias con casos de uso distintos.
* **Spark escala mejor cuando el volumen crece.** El punto de inflexión típicamente está entre 1-10 GB.
* **El cambio importante no es la sintaxis, sino el modelo de ejecución.** Spark distribuye el trabajo; pandas es single-machine.
* **En Big Data real se combinan ambas herramientas.** Spark para procesar, pandas para análisis exploratorio.
* **El overhead importa:** Iniciar Spark, serializar datos, coordinación entre nodos. Solo se justifica con volúmenes significativos.

---

## 10. Lo que viene después

En el siguiente bloque:

* Trabajaremos con formatos eficientes (Parquet).
* Prepararemos datos para visualización en Kibana.
* Usaremos herramientas específicas de Big Data (Hive, HBase).
* Automatizaremos procesos con Airflow.

👉 **No corras**: lo importante aquí es entender el porqué, no la velocidad.

---

## 11. Próximas pruebas recomendadas

Para profundizar en este laboratorio, prueba:

1. **Aumentar el factor:** Usa `--factor 10000` y mide de nuevo
2. **Monitorear recursos:** Abre el gestor de tareas mientras ejecutas
3. **Usar formatos más grandes:** CSV vs Parquet vs JSON
4. **Ejecutar en el cluster Spark:** Compara tiempos locales vs distribuidos
5. **Profiling:** Usa `cProfile` en pandas y `Spark UI` en Spark
* El cambio importante no es la sintaxis, sino el modelo de ejecución.
* En Big Data real se combinan ambas herramientas.

---

## 10. Lo que viene después

En el siguiente bloque:

* Trabajaremos con formatos eficientes (Parquet).
* Prepararemos datos para visualización.
* Usaremos herramientas específicas de Big Data.

👉 **No corras**: lo importante aquí es entender el porqué.




