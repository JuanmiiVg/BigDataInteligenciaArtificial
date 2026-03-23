# Proyecto Airflow - Laboratorio básico

## Arranque
1. Abrir terminal en esta carpeta.
2. Ejecutar:

```powershell
docker compose up -d
```

3. Acceder a Airflow:
- URL: http://localhost:8081
- Usuario: admin
- Password: admin

## DAG
- DAG: `pipeline_basico`
- Tareas: `descarga -> limpieza -> procesamiento -> guardado`

## Capturas sugeridas
- `capturas/01_dag_graph.png` (vista Graph del DAG ejecutado)
- `capturas/02_logs_tarea.png` (logs de una tarea)
- `capturas/03_run_success.png` (run con estado success)

## Parar entorno

```powershell
docker compose down
```
