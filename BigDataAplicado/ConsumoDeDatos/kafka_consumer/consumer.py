"""
Consumidor Kafka con detección de anomalías y persistencia en MongoDB y PostgreSQL
"""
import json
import sys
import os
from datetime import datetime, timedelta
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import logging
from typing import Dict, List, Optional
import numpy as np
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    KAFKA_BROKER, KAFKA_TOPIC_CONSUMOS, KAFKA_TOPIC_ANOMALIAS,
    KAFKA_GROUP_ID, MONGO_URI, MONGO_DB, COLLECTION_CONSUMOS,
    COLLECTION_CONSUMOS_DIARIOS, COLLECTION_ANOMALIAS,
    ANOMALY_PERCENTILE, SPIKE_THRESHOLD_PERCENT, NIGHT_HOURS,
    PEAK_HOURS, NIGHT_RATIO_THRESHOLD
)
from kafka_consumer.db_postgres import PostgresDataStore

try:
    from pymongo import MongoClient, UpdateOne, ASCENDING
except ImportError:
    logging.error("pymongo no instalado. Instala con: pip install pymongo")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AnomalyDetector:
    """Detecta anomalías en consumos"""
    
    def __init__(self, ventana_horas: int = 24):
        self.ventana_horas = ventana_horas
        self.historial_clientes: Dict[str, deque] = {}
        self.estadisticas: Dict[str, Dict] = {}
    
    def agregar_consumo(self, propietario_id: str, consumo: float, hora: int):
        """Agrega consumo al historial"""
        if propietario_id not in self.historial_clientes:
            self.historial_clientes[propietario_id] = deque(maxlen=self.ventana_horas)
            self.estadisticas[propietario_id] = {
                'consumos': [],
                'promedio': 0,
                'desviacion': 0,
                'min': float('inf'),
                'max': 0
            }
        
        self.historial_clientes[propietario_id].append({
            'consumo': consumo,
            'hora': hora,
            'timestamp': datetime.now().isoformat()
        })
        
        # Actualizar estadísticas
        self._actualizar_estadisticas(propietario_id)
    
    def _actualizar_estadisticas(self, propietario_id: str):
        """Actualiza estadísticas del cliente"""
        consumos = [r['consumo'] for r in self.historial_clientes[propietario_id]]
        
        if consumos:
            self.estadisticas[propietario_id]['consumos'] = consumos
            self.estadisticas[propietario_id]['promedio'] = np.mean(consumos)
            self.estadisticas[propietario_id]['desviacion'] = np.std(consumos)
            self.estadisticas[propietario_id]['min'] = np.min(consumos)
            self.estadisticas[propietario_id]['max'] = np.max(consumos)
    
    def detectar_anomalias(self, propietario_id: str, consumo: float, hora: int) -> Dict:
        """Detecta si hay anomalía en el consumo actual"""
        anomalia = {
            'detectada': False,
            'tipos': [],
            'score': 0.0,
            'severidad': 'normal'
        }
        
        if propietario_id not in self.estadisticas:
            return anomalia
        
        stats = self.estadisticas[propietario_id]
        promedio = stats['promedio']
        desviacion = stats['desviacion']
        
        if promedio == 0:
            return anomalia
        
        # 1. Detección de pico (spike)
        z_score = (consumo - promedio) / (desviacion + 1e-6)
        if z_score > 3:  # Más de 3 desviaciones estándar
            anomalia['detectada'] = True
            anomalia['tipos'].append('pico_anomalo')
            anomalia['score'] += 0.4
        
        # 2. Detección de consumo muy alto
        incremento_percent = ((consumo - promedio) / promedio * 100) if promedio > 0 else 0
        if incremento_percent > SPIKE_THRESHOLD_PERCENT:
            anomalia['detectada'] = True
            anomalia['tipos'].append('consumo_elevado')
            anomalia['score'] += 0.3
        
        # 3. Consumo anómalo en horario de noche (posible plantación)
        if hora in NIGHT_HOURS and consumo > promedio * 2:
            anomalia['detectada'] = True
            anomalia['tipos'].append('consumo_noche_anomalo')
            anomalia['score'] += 0.3
        
        # Determinar severidad
        if anomalia['score'] > 0.7:
            anomalia['severidad'] = 'crítica'
        elif anomalia['score'] > 0.5:
            anomalia['severidad'] = 'alta'
        elif anomalia['detectada']:
            anomalia['severidad'] = 'media'
        
        return anomalia

class ConsumptionConsumer:
    """Consumidor Kafka con persistencia en MongoDB y PostgreSQL"""
    
    def __init__(self, bootstrap_servers=KAFKA_BROKER):
        self.bootstrap_servers = bootstrap_servers
        self.consumer = None
        self.mongo_client = None
        self.db = None
        self.postgres_store = None
        self.detector = AnomalyDetector()
        self.productor_anomalias = None
    
    def conectar_kafka(self):
        """Conecta al consumer Kafka"""
        try:
            self.consumer = KafkaConsumer(
                KAFKA_TOPIC_CONSUMOS,
                bootstrap_servers=self.bootstrap_servers,
                group_id=KAFKA_GROUP_ID,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                max_poll_records=500
            )
            logger.info(f"✓ Consumer Kafka conectado: {self.bootstrap_servers}")
            logger.info(f"✓ Topic: {KAFKA_TOPIC_CONSUMOS}")
        except Exception as e:
            logger.error(f"✗ Error conectando a Kafka: {e}")
            raise
    
    def conectar_mongodb(self):
        """Conecta a MongoDB"""
        try:
            self.mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            self.mongo_client.server_info()  # Test connection
            self.db = self.mongo_client[MONGO_DB]
            
            # Crear índices
            self._crear_indices()
            
            logger.info(f"✓ MongoDB conectado: {MONGO_URI}")
            logger.info(f"✓ BD: {MONGO_DB}")
        except Exception as e:
            logger.error(f"✗ Error conectando a MongoDB: {e}")
            raise
    
    def _crear_indices(self):
        """Crea índices en MongoDB"""
        try:
            coll_consumos = self.db[COLLECTION_CONSUMOS]
            coll_consumos.create_index([("propietario_id", ASCENDING)])
            coll_consumos.create_index([("timestamp", ASCENDING)])
            coll_consumos.create_index([("propietario_id", ASCENDING), ("timestamp", ASCENDING)])
            
            coll_anomalias = self.db[COLLECTION_ANOMALIAS]
            coll_anomalias.create_index([("propietario_id", ASCENDING)])
            coll_anomalias.create_index([("timestamp_deteccion", ASCENDING)])
            coll_anomalias.create_index([("severidad", ASCENDING)])
            
            logger.info("✓ Índices creados en MongoDB")
        except Exception as e:
            logger.warning(f"⚠ Error creando índices: {e}")
    
    def conectar_postgres(self):
        """Conecta a PostgreSQL"""
        try:
            self.postgres_store = PostgresDataStore()
            self.postgres_store.conectar()
            logger.info("✓ PostgreSQL conectado")
        except Exception as e:
            logger.error(f"✗ Error conectando a PostgreSQL: {e}")
            # No lanzar excepción si PostgreSQL falla - continuar con MongoDB
            self.postgres_store = None
    
    def procesar_consumo(self, consumo_data: dict):
        """Procesa un registro de consumo"""
        try:
            propietario_id = consumo_data.get('propietario_id')
            consumo_kwh = consumo_data.get('consumo_kwh', 0)
            hora = consumo_data.get('hora', 0)
            timestamp = consumo_data.get('timestamp')
            
            # Agregar al historial
            self.detector.agregar_consumo(propietario_id, consumo_kwh, hora)
            
            # Detectar anomalías
            anomalia = self.detector.detectar_anomalias(propietario_id, consumo_kwh, hora)
            
            # Documento a guardar
            doc = {
                'propietario_id': propietario_id,
                'timestamp': timestamp,
                'hora': hora,
                'consumo_kwh': consumo_kwh,
                'anomalia_detectada': anomalia['detectada'],
                'tipos_anomalia': anomalia['tipos'],
                'score_anomalia': anomalia['score'],
                'severidad': anomalia['severidad'],
                'es_sospechoso': consumo_data.get('es_sospechoso', False),
                'anomalia_esperada': consumo_data.get('anomalia_esperada', False),
                'tipo_anomalia_esperada': consumo_data.get('tipo_anomalia'),
                'timestamp_procesado': datetime.now().isoformat()
            }
            
            # Guardar en PostgreSQL (consumos diarios)
            if self.postgres_store:
                try:
                    self.postgres_store.guardar_consumo(doc)
                except Exception as e:
                    logger.warning(f"⚠ Error guardando en PostgreSQL: {e}")
            
            # Guardar en MongoDB (anomalías)
            coll = self.db[COLLECTION_CONSUMOS]
            coll.insert_one(doc)
            
            # Si es anomalía, guardar también en colección de anomalías
            if anomalia['detectada']:
                self._guardar_anomalia(doc, anomalia)
                logger.warning(
                    f"🚨 ANOMALÍA DETECTADA: {propietario_id} - "
                    f"Consumo: {consumo_kwh}kW - Severidad: {anomalia['severidad']} - "
                    f"Tipos: {anomalia['tipos']}"
                )
            
            return doc
        
        except Exception as e:
            logger.error(f"✗ Error procesando consumo: {e}")
            return None
    
    def _guardar_anomalia(self, consumo_doc: dict, anomalia: dict):
        """Guarda anomalía en colección especial"""
        try:
            anomalia_doc = {
                'propietario_id': consumo_doc['propietario_id'],
                'timestamp_consumo': consumo_doc['timestamp'],
                'timestamp_deteccion': datetime.now().isoformat(),
                'consumo_kwh': consumo_doc['consumo_kwh'],
                'hora': consumo_doc['hora'],
                'tipos_anomalia': anomalia['tipos'],
                'score_anomalia': anomalia['score'],
                'severidad': anomalia['severidad'],
                'es_sospechoso_cliente': consumo_doc.get('es_sospechoso', False),
                'anomalia_esperada': consumo_doc.get('anomalia_esperada', False),
                'tipo_anomalia_esperada': consumo_doc.get('tipo_anomalia_esperada')
            }
            
            coll = self.db[COLLECTION_ANOMALIAS]
            coll.insert_one(anomalia_doc)
        
        except Exception as e:
            logger.error(f"✗ Error guardando anomalía: {e}")
    
    def consumir(self):
        """Inicia el consumo continuo de mensajes"""
        logger.info(f"🔄 Escuchando mensajes en {KAFKA_TOPIC_CONSUMOS}...")
        
        try:
            for mensaje in self.consumer:
                consumo_data = mensaje.value
                self.procesar_consumo(consumo_data)
        
        except KeyboardInterrupt:
            logger.info("\n⏹️ Consumer detenido por el usuario")
        except Exception as e:
            logger.error(f"Error en consumer: {e}")
        finally:
            self.desconectar()
    
    def desconectar(self):
        """Desconecta del consumer, MongoDB y PostgreSQL"""
        if self.consumer:
            self.consumer.close()
            logger.info("Consumer Kafka desconectado")
        
        if self.postgres_store:
            self.postgres_store.desconectar()
            logger.info("PostgreSQL desconectado")
        
        if self.mongo_client:
            self.mongo_client.close()
            logger.info("MongoDB desconectado")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Consumidor Kafka de consumos")
    parser.add_argument("--broker", default=KAFKA_BROKER,
                       help=f"Broker de Kafka (default: {KAFKA_BROKER})")
    parser.add_argument("--mongo", default=MONGO_URI,
                       help=f"URI de MongoDB (default: {MONGO_URI})")
    
    args = parser.parse_args()
    
    consumer = ConsumptionConsumer(bootstrap_servers=args.broker)
    
    try:
        consumer.conectar_kafka()
        consumer.conectar_mongodb()
        consumer.conectar_postgres()
        consumer.consumir()
    except Exception as e:
        logger.error(f"Error fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
