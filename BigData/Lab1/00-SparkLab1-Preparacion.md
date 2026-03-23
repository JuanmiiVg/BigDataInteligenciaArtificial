# Laboratorio 1 — Preparación y primer uso de Spark
## UD3 · Procesamiento distribuido

En este laboratorio vamos a **trabajar por primera vez con Apache Spark**, un motor de procesamiento distribuido usado cuando los datos son grandes y no se pueden tratar cómodamente con pandas.

⚠️ **Importante**  
No todos los grupos trabajarán exactamente igual.  
Eso es normal y **no afecta a la nota ni al aprendizaje**.

---

## 1. ¿Qué vamos a hacer en este laboratorio?

- Preparar un entorno Spark usando Docker.
- Ejecutar un programa PySpark sencillo.
- Procesar un dataset que ya conoces (integrado y anonimizado).
- Entender **qué cambia respecto a pandas**.

👉 El objetivo **no es aprender toda Spark**, sino comprender el modelo.

---

## 2. Roles en el grupo

Trabajaremos normalmente en **grupos de 3 personas**:

- **1 alumno/a → Spark Master**
- **2 alumnos/as → Spark Workers**

> El rol puede cambiar en otras sesiones.

---

## 3. Requisitos mínimos

Cada alumno debe tener:

- Docker y Docker Compose funcionando.
- El proyecto descargado (ZIP o Git).
- El fichero de datos en la carpeta `data/`.

Todos debéis estar **en la misma red** si vais a usar varias máquinas.

---

## 4. Estructura del proyecto

Todos trabajamos con la misma estructura:

```

ud3-spark-lab1/
docker-compose.master.yml
docker-compose.worker.yml
apps/
lab1_job.py
data/
ventas_clientes_anon.csv

````

⚠️ **Muy importante**  
El fichero `ventas_clientes_anon.csv` debe existir en **todas las máquinas**, en la carpeta `data/`.

---

## 5. Arrancar Spark (Plan A o Plan B)

Dependiendo de la red, usaremos uno de estos planes.

---

## 🅰️ Plan A — Varias máquinas (ideal)

Usa este plan si los portátiles **se ven entre sí por IP**.

### 5.1 Arrancar el Master

En el portátil que hará de **Master**:

```bash
export MASTER_IP=192.168.1.50   # IP real del portátil master
docker compose -f docker-compose.master.yml up -d
````

Comprueba que funciona:

* Navegador → `http://localhost:8080`

---

### 5.2 Arrancar los Workers

En cada portátil Worker:

```bash
export MASTER_IP=192.168.1.50   # IP del master
docker compose -f docker-compose.worker.yml up -d
```

En la web del Master (`:8080`) deberían aparecer los Workers conectados.

---

## 🅱️ Plan B — Una sola máquina (muy habitual)

Si la red **no permite conexiones entre portátiles**, no pasa nada.

👉 **Master y Worker se ejecutan en el mismo portátil**.

```bash
export MASTER_IP=127.0.0.1
docker compose -f docker-compose.master.yml up -d
docker compose -f docker-compose.worker.yml up -d
```

Mensaje importante:

> Aunque esté todo en el mismo portátil,
> **Spark sigue siendo distribuido** (procesos distintos).

---

## 🅲 Plan C — Spark local (solo si todo falla)

Si tienes problemas graves:

```bash
docker exec -it spark-master spark-submit \
  --master local[*] \
  /opt/spark-apps/lab1_job.py
```

⚠️ Este plan **funciona**, pero no muestra bien el clúster.

---

## 6. Ejecutar el programa Spark

Este paso lo hace **el Master**.

```bash
docker exec -it spark-master spark-submit \
  --master spark://IP_DEL_MASTER:7077 \
  /opt/spark-apps/lab1_job.py
```

Sustituye `IP_DEL_MASTER` por la IP correcta.

---

## 7. ¿Qué hace el programa `lab1_job.py`?

De forma sencilla:

1. Lee el CSV con Spark.
2. Muestra el esquema y algunas filas.
3. Filtra ventas con importe mayor de 100.
4. Agrupa por ciudad.
5. Calcula:

   * número de ventas
   * importe total
   * importe medio
6. Guarda el resultado en un CSV.

👉 Son operaciones **muy parecidas a pandas**, pero ejecutadas de forma distribuida.

---

## 8. Resultado del procesamiento

El resultado se guarda en:

```
data/output/ventas_por_ciudad/
```

Verás una carpeta con un fichero `part-*.csv`.

Esto es normal en Spark.

---

## 9. Problemas habituales y soluciones rápidas

### ❌ No aparecen Workers

* ¿Estáis en la misma red?
* ¿La IP del Master es correcta?
* ¿El Master no usa `localhost` por error?

---

### ❌ Error al leer el CSV

* Comprueba que **todas las máquinas** tienen el CSV.
* No cambies la ruta del fichero.

---

## 10. Qué deberías entender al terminar

Al finalizar este laboratorio deberías poder explicar:

* Qué es un Spark Master y un Worker.
* Qué significa procesamiento distribuido.
* En qué se parece y en qué se diferencia Spark de pandas.
* Por qué Spark es útil cuando el volumen crece.

---

## 11. Lo que viene después

En el siguiente laboratorio:

* Inflaremos el dataset (muchos más datos).
* Compararemos tiempos con pandas.
* Usaremos formatos como Parquet.
* Prepararemos resultados para visualización.

---

👉 **Si algo no funciona, pregunta**.
En Big Data real, la infraestructura nunca es perfecta.






