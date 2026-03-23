#!/usr/bin/env python3
"""
Script para generar logs simulados de una aplicación web
Simula errores, warnings e info de un servidor
"""

import requests
import json
from datetime import datetime, timedelta
import random
import time

ELASTICSEARCH_URL = "http://localhost:9200"
INDEX_NAME = "app-logs"

# Tipos de log
LOG_LEVELS = ["INFO", "WARNING", "ERROR"]
SERVICES = ["auth-service", "api-gateway", "database", "cache", "payment-service"]
HOSTS = ["server-01", "server-02", "server-03", "server-04"]

# Mensajes de ejemplo
INFO_MESSAGES = [
    "User login successful",
    "Request processed successfully",
    "Cache hit",
    "Database query executed",
    "Payment processed",
    "File uploaded"
]

WARNING_MESSAGES = [
    "High CPU usage detected",
    "Database connection slow",
    "Cache miss rate increasing",
    "Memory usage above 80%",
    "Response time degradation",
    "Queue size growing"
]

ERROR_MESSAGES = [
    "Database connection failed",
    "Timeout error",
    "Authentication failed",
    "Payment gateway error",
    "Out of memory exception",
    "Service unavailable",
    "Invalid request format",
    "Disk space critical"
]

def crear_indice():
    """Crea el índice en Elasticsearch"""
    url = f"{ELASTICSEARCH_URL}/{INDEX_NAME}"
    
    mapping = {
        "mappings": {
            "properties": {
                "timestamp": {"type": "date"},
                "level": {"type": "keyword"},
                "service": {"type": "keyword"},
                "host": {"type": "keyword"},
                "message": {"type": "text"},
                "response_time_ms": {"type": "integer"},
                "status_code": {"type": "integer"},
                "user_id": {"type": "keyword"},
                "request_id": {"type": "keyword"},
                "error_code": {"type": "keyword"}
            }
        }
    }
    
    # Eliminar índice si existe
    requests.delete(url)
    
    # Crear nuevo índice
    response = requests.put(url, json=mapping)
    print(f"Índice creado: {response.status_code}")
    return response.status_code == 200

def generar_logs(num_logs=1000):
    """Genera logs simulados"""
    logs = []
    fecha_base = datetime.now() - timedelta(days=7)  # Últimos 7 días
    
    for i in range(num_logs):
        # Distribuir logs a lo largo de 7 días
        timestamp = fecha_base + timedelta(
            days=random.randint(0, 6),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        # 70% INFO, 20% WARNING, 10% ERROR
        rand = random.random()
        if rand < 0.70:
            level = "INFO"
            message = random.choice(INFO_MESSAGES)
            status_code = 200
            response_time = random.randint(10, 500)
        elif rand < 0.90:
            level = "WARNING"
            message = random.choice(WARNING_MESSAGES)
            status_code = 202
            response_time = random.randint(500, 2000)
        else:
            level = "ERROR"
            message = random.choice(ERROR_MESSAGES)
            status_code = random.choice([400, 401, 403, 404, 500, 502, 503])
            response_time = random.randint(1000, 5000)
        
        log = {
            "timestamp": timestamp.isoformat(),
            "level": level,
            "service": random.choice(SERVICES),
            "host": random.choice(HOSTS),
            "message": message,
            "response_time_ms": response_time,
            "status_code": status_code,
            "user_id": f"user_{random.randint(1, 100)}",
            "request_id": f"req_{i}_{random.randint(1000, 9999)}",
            "error_code": random.choice([None, "ERR001", "ERR002", "ERR003", "ERR404"]) if level == "ERROR" else None
        }
        logs.append(log)
    
    return logs

def cargar_datos(logs):
    """Carga los logs en Elasticsearch usando Bulk API"""
    url = f"{ELASTICSEARCH_URL}/_bulk"
    
    bulk_data = []
    for log in logs:
        bulk_data.append(json.dumps({"index": {"_index": INDEX_NAME}}))
        bulk_data.append(json.dumps(log))
    
    bulk_body = "\n".join(bulk_data) + "\n"
    
    headers = {"Content-Type": "application/x-ndjson"}
    response = requests.post(url, data=bulk_body, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        errores = [item for item in result['items'] if 'error' in item.get('index', {})]
        if errores:
            print(f"⚠️  Se encontraron {len(errores)} errores")
        else:
            print(f"✅ {len(logs)} logs cargados correctamente")
    else:
        print(f"❌ Error al cargar logs: {response.status_code}")
        print(response.text)
    
    return response.status_code == 200

def verificar_datos():
    """Verifica cuántos documentos se han cargado"""
    url = f"{ELASTICSEARCH_URL}/{INDEX_NAME}/_count"
    response = requests.get(url)
    
    if response.status_code == 200:
        count = response.json()['count']
        print(f"\n📊 Total de logs en el índice '{INDEX_NAME}': {count}")
        
        # Estadísticas por nivel
        stats_url = f"{ELASTICSEARCH_URL}/{INDEX_NAME}/_search"
        aggs = {
            "aggs": {
                "logs_por_nivel": {
                    "terms": {"field": "level", "size": 10}
                }
            }
        }
        stats_response = requests.post(stats_url, json=aggs)
        if stats_response.status_code == 200:
            buckets = stats_response.json()['aggregations']['logs_por_nivel']['buckets']
            print("\n📈 Distribución por nivel:")
            for bucket in buckets:
                print(f"  {bucket['key']}: {bucket['doc_count']} logs")
    else:
        print(f"❌ Error al verificar datos: {response.status_code}")

def main():
    print("🚀 Generando logs simulados en Elasticsearch...\n")
    
    # Crear índice
    if not crear_indice():
        print("❌ Error al crear el índice")
        return
    
    # Generar y cargar logs
    print("📦 Generando 1000 logs...")
    logs = generar_logs(1000)
    
    print(f"⬆️  Cargando logs en Elasticsearch...")
    if cargar_datos(logs):
        time.sleep(2)  # Esperar a que se indexe
        verificar_datos()
        print("\n✅ ¡Logs cargados con éxito!")
        print(f"👉 Accede a Kibana: http://localhost:5601")
    else:
        print("\n❌ Hubo un problema al cargar los logs")

if __name__ == "__main__":
    main()
