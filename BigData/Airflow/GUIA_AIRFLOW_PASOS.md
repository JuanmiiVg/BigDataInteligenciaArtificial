# Guía paso a paso - Laboratorio Airflow básico

## 1) Levantar entorno
En terminal, situarte en `BigData/Airflow/proyecto_airflow` y ejecutar:

```powershell
docker compose up -d
```

## 2) Abrir interfaz
- URL: http://localhost:8081
- Usuario: `admin`
- Password: `admin`

## 3) Activar y ejecutar DAG
1. Buscar DAG `pipeline_basico`.
2. Activarlo con el switch.
3. Lanzar ejecución manual (Trigger DAG).

## 4) Revisar resultados
- En vista **Graph** comprobar secuencia `descarga -> limpieza -> procesamiento -> guardado`.
- Abrir logs de una tarea (por ejemplo `procesamiento`).

## 5) Capturas obligatorias
Guardar en `proyecto_airflow/capturas/`:
- `01_dag_graph.png` → vista Graph con DAG ejecutado.
- `02_logs_tarea.png` → logs de una tarea.
- `03_run_success.png` → ejecución completa en success.

## 6) Entrega
- Documento: `UD4_Lab_Airflow_Entrega.md` (ya pre-rellenado).
- Copiar documento y capturas a `AirflowEntrega/`.
- Comprimir `AirflowEntrega` y enviar.
