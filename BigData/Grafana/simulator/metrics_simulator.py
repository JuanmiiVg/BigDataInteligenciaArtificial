#!/usr/bin/env python3
"""
Simulador de métricas para el laboratorio de Grafana
Genera métricas fake de CPU y peticiones HTTP para visualización
"""

import time
import random
import threading
from prometheus_client import start_http_server, Gauge, Counter
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear métricas de Prometheus
fake_cpu_usage = Gauge(
    'fake_cpu_usage',
    'Uso simulado de CPU en porcentaje'
)

fake_requests_total = Counter(
    'fake_requests_total',
    'Número total de peticiones HTTP simuladas'
)

fake_memory_usage = Gauge(
    'fake_memory_usage_bytes',
    'Uso simulado de memoria en bytes'
)

def simulate_cpu_usage():
    """Simula el uso de CPU con variaciones realistas"""
    base_cpu = 20  # CPU base del 20%
    
    while True:
        # Generar variaciones realistas de CPU
        variation = random.uniform(-10, 30)
        cpu_value = max(0, min(100, base_cpu + variation))
        
        # Simular picos ocasionales
        if random.random() < 0.1:  # 10% de probabilidad
            cpu_value = random.uniform(70, 95)
        
        fake_cpu_usage.set(cpu_value)
        logger.info(f"CPU Usage: {cpu_value:.2f}%")
        
        time.sleep(2)

def simulate_requests():
    """Simula peticiones HTTP entrantes"""
    while True:
        # Simular diferentes patrones de tráfico
        if random.random() < 0.7:  # Tráfico normal
            requests_increment = random.randint(1, 5)
        elif random.random() < 0.9:  # Tráfico medio
            requests_increment = random.randint(5, 15)
        else:  # Pico de tráfico
            requests_increment = random.randint(20, 50)
        
        for _ in range(requests_increment):
            fake_requests_total.inc()
        
        logger.info(f"Added {requests_increment} requests")
        
        time.sleep(random.uniform(1, 3))

def simulate_memory_usage():
    """Simula el uso de memoria"""
    base_memory = 500 * 1024 * 1024  # 500MB base
    
    while True:
        variation = random.uniform(-100, 200) * 1024 * 1024  # ±200MB
        memory_value = max(100*1024*1024, base_memory + variation)  # Mínimo 100MB
        
        fake_memory_usage.set(memory_value)
        logger.info(f"Memory Usage: {memory_value / 1024 / 1024:.2f} MB")
        
        time.sleep(5)

def main():
    """Función principal que inicia el servidor y las simulaciones"""
    logger.info("🚀 Iniciando simulador de métricas...")
    logger.info("📊 Métricas disponibles:")
    logger.info("   - fake_cpu_usage: Uso de CPU simulado")
    logger.info("   - fake_requests_total: Contador de peticiones")
    logger.info("   - fake_memory_usage_bytes: Uso de memoria simulado")
    logger.info("🌐 Servidor de métricas en puerto 8000")
    
    # Iniciar servidor de métricas de Prometheus
    start_http_server(8000)
    
    # Iniciar threads para simular diferentes métricas
    cpu_thread = threading.Thread(target=simulate_cpu_usage, daemon=True)
    requests_thread = threading.Thread(target=simulate_requests, daemon=True)
    memory_thread = threading.Thread(target=simulate_memory_usage, daemon=True)
    
    cpu_thread.start()
    requests_thread.start()
    memory_thread.start()
    
    logger.info("✅ Simulador iniciado correctamente")
    logger.info("🔗 Acceso a métricas: http://localhost:8000/metrics")
    
    try:
        # Mantener el programa ejecutándose
        while True:
            time.sleep(10)
            logger.info("🔄 Simulador funcionando correctamente...")
    
    except KeyboardInterrupt:
        logger.info("🛑 Deteniendo simulador...")

if __name__ == '__main__':
    main()