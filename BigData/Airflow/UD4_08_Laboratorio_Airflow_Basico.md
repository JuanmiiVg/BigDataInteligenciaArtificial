# UD4 - Laboratorio
## Orquestación básica de un pipeline con Airflow

---

# 1. Objetivo del laboratorio

En este laboratorio el alumnado deberá:

- Levantar Airflow mediante contenedores.
- Crear un DAG sencillo.
- Ejecutar el DAG manualmente.
- Observar dependencias y estados.
- Comprender el flujo completo.

No se evaluará configuración avanzada.
Se evaluará comprensión del pipeline.

---

# 2. Arquitectura del laboratorio

El DAG representará el siguiente flujo:

Tarea 1 -> Descargar datos
Tarea 2 -> Limpieza
Tarea 3 -> Procesamiento
Tarea 4 -> Guardar resultado

Cada tarea será un script Python simple.

---

# 3. Estructura del proyecto

Crear la siguiente estructura:

proyecto_airflow/
  docker-compose.yml
  dags/
    pipeline_basico.py
  scripts/
    descarga.py
    limpieza.py
    procesamiento.py
    guardado.py

---

# 4. docker-compose.yml mínimo

Usaremos la imagen oficial de Airflow.

```yaml
version: "3"

services:
  airflow:
    image: apache/airflow:2.8.4
    container_name: airflow_lab
    environment:
      - AIRFLOW__CORE__LOAD_EXAMPLES=False
      - AIRFLOW__CORE__EXECUTOR=SequentialExecutor
      - AIRFLOW__CORE__FERNET_KEY=
    volumes:
      - ./dags:/opt/airflow/dags
      - ./scripts:/opt/airflow/scripts
    ports:
      - "8081:8080"
    command: >
      bash -c "
      airflow db init &&
      airflow users create --username admin --password admin --firstname admin --lastname admin --role Admin --email admin@admin.com &&
      airflow webserver & airflow scheduler
      "
````

Nota:
Este entorno usa SequentialExecutor para simplificar.
Todo corre en un solo contenedor.

---

# 5. Scripts de ejemplo

## descarga.py

```python
print("Descargando datos...")
```

## limpieza.py

```python
print("Limpiando datos...")
```

## procesamiento.py

```python
print("Procesando datos...")
```

## guardado.py

```python
print("Guardando resultados...")
```

---

# 6. Definición del DAG

Archivo: dags/pipeline_basico.py

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    dag_id="pipeline_basico",
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
) as dag:

    descarga = BashOperator(
        task_id="descarga",
        bash_command="python /opt/airflow/scripts/descarga.py",
    )

    limpieza = BashOperator(
        task_id="limpieza",
        bash_command="python /opt/airflow/scripts/limpieza.py",
    )

    procesamiento = BashOperator(
        task_id="procesamiento",
        bash_command="python /opt/airflow/scripts/procesamiento.py",
    )

    guardado = BashOperator(
        task_id="guardado",
        bash_command="python /opt/airflow/scripts/guardado.py",
    )

    descarga >> limpieza >> procesamiento >> guardado
```

La última línea define las dependencias.

---

# 7. Ejecución

1. Ejecutar:

   docker compose up

2. Acceder a:

   [http://localhost:8081](http://localhost:8081)

3. Usuario: admin
   Password: admin

4. Activar el DAG.

5. Ejecutarlo manualmente.

6. Observar el flujo.

---

# 8. Análisis del flujo

Observar:

* Estado de cada tarea.
* Dependencias.
* Logs.
* Tiempo de ejecución.

Responder:

1. ¿Qué ocurre si una tarea falla?
2. ¿Cómo se refleja en la interfaz?
3. ¿Qué ventaja tiene frente a ejecutar scripts manualmente?

---

# 9. Extensión opcional

Modificar el DAG para:

* Añadir una tarea intermedia.
* Introducir una dependencia paralela.
* Simular error en un script.

---

# 10. Entregable

Documento PDF con:

* Captura del DAG ejecutado.
* Captura de logs.
* Respuestas razonadas.
* Explicación del flujo.

---

# 11. Conclusiones

El laboratorio demuestra:

* Qué es un DAG.
* Cómo se definen dependencias.
* Cómo se automatiza un flujo.
* Cómo se monitoriza.

Airflow no procesa datos.
Coordina procesos.

---

## Fin del laboratorio


