# Lab 3 — CSV → Parquet (local)

Archivos añadidos para ejecutar el laboratorio localmente:

- `apps/lab3_parquet_job.py`: convierte `data/ventas_clientes_anon_big.csv` a Parquet. Usa Spark en modo local.
- `apps/lab3_explore.py`: lee el Parquet, muestra agregaciones y guarda una gráfica en `data/figures/ventas_por_ciudad.png`.
- `requirements.txt`: dependencias sugeridas para entorno local.

Instrucciones rápidas:

1. Crear y activar un entorno virtual (recomendado):

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar la conversión CSV → Parquet (sin particionar):

```bash
python apps/lab3_parquet_job.py
```

4. Ejecutar la conversión particionada por `ciudad`:

```bash
python apps/lab3_parquet_job.py --partition
```

5. Explorar y generar gráfica:

```bash
python apps/lab3_explore.py
```

6. Abrir un notebook Jupyter (opcional) y ejecutar comandos PySpark similares para exploración interactiva:

```bash
jupyter notebook
```

Notas:

- Los scripts usan Spark en modo local (`local[*]`). Si tienes un clúster, modifica `SparkSession` según corresponda.
- Las rutas usadas por defecto quedan en `data/` dentro del proyecto: `data/ventas_clientes_anon_big.csv` y `data/parquet/ventas/`.
