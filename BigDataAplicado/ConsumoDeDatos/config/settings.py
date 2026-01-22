"""
Configuración centralizada para el sistema de monitoreo de consumo
"""
import os
from dataclasses import dataclass

# ========== POSTGRES SQL (Histórico de consumos diarios) ==========
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "consumo_db")
POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# ========== MONGO DB (Datos mensuales agregados) ==========
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "password")
MONGO_DB = os.getenv("MONGO_DB", "consumo_db")
# URI con autenticación
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"

# Colecciones
COLLECTION_CONSUMOS = "consumos_horarios"
COLLECTION_CONSUMOS_DIARIOS = "consumos_diarios"
COLLECTION_CONSUMOS_MENSUALES = "consumos_mensuales"
COLLECTION_ANOMALIAS = "anomalias_detectadas"
COLLECTION_CLIENTES = "clientes"

# ========== KAFKA ==========
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC_CONSUMOS = "consumos-data"
KAFKA_TOPIC_ANOMALIAS = "anomalias-detectadas"
KAFKA_GROUP_ID = "consumo-processor-group"

# ========== DETECCIÓN DE ANOMALÍAS ==========
# Percentil para considerar consumo anómalo
ANOMALY_PERCENTILE = float(os.getenv("ANOMALY_PERCENTILE", 95.0))

# Ratio noche vs día anómalo
NIGHT_RATIO_THRESHOLD = float(os.getenv("NIGHT_RATIO_THRESHOLD", 1.5))

# Detección de picos repentinos (repunte > X% respecto promedio)
SPIKE_THRESHOLD_PERCENT = float(os.getenv("SPIKE_THRESHOLD_PERCENT", 150.0))

# Horas de noche (0-6, 23)
NIGHT_HOURS = list(range(0, 6)) + [23]

# Horas de punta (18-22)
PEAK_HOURS = list(range(18, 23))

# ========== API ==========
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_RELOAD = os.getenv("API_RELOAD", "True").lower() == "true"

# ========== FRONTEND ==========
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", 8501))

# ========== GENERADOR DE DATOS ==========
# Número de clientes a generar
NUM_CLIENTES = int(os.getenv("NUM_CLIENTES", 50))

# Consumo base promedio (kW)
BASE_CONSUMPTION = float(os.getenv("BASE_CONSUMPTION", 0.5))

# Consumo punta (kW)
PEAK_CONSUMPTION = float(os.getenv("PEAK_CONSUMPTION", 2.0))

# Consumo noche (kW)
NIGHT_CONSUMPTION = float(os.getenv("NIGHT_CONSUMPTION", 0.1))

# Porcentaje de clientes sospechosos
SUSPICIOUS_PERCENT = float(os.getenv("SUSPICIOUS_PERCENT", 10.0))

# ========== MÁRGENES DE ERROR ==========
CONSUMPTION_VARIANCE = float(os.getenv("CONSUMPTION_VARIANCE", 0.2))  # 20% de varianza

@dataclass
class AnomalyThresholds:
    """Umbrales para diferentes tipos de anomalías"""
    high_consumption: float = ANOMALY_PERCENTILE
    night_ratio: float = NIGHT_RATIO_THRESHOLD
    spike_threshold: float = SPIKE_THRESHOLD_PERCENT
