# Kit de Aula — UD3 Spark Standalone (Master + Workers)

## Versión de Spark
- **Apache Spark 3.5.4** (versión estable usada en el curso)

## Estructura
- docker-compose.master.yml
- docker-compose.worker.yml
- apps/
- data/
- scripts/

## Pasos rápidos
1. Elegir un alumno como MASTER.
2. MASTER:
   export MASTER_IP=IP_LAN
   docker compose -f docker-compose.master.yml up -d
3. WORKERS:
   export MASTER_IP=IP_LAN_DEL_MASTER
   docker compose -f docker-compose.worker.yml up -d
4. Ejecutar job desde MASTER:
   docker exec -it spark-master spark-submit --master spark://IP_LAN:7077 /opt/spark-apps/lab1_job.py
