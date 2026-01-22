"""
Productor Kafka que envía datos de consumo
"""
import json
import time
import sys
import os
from datetime import datetime, timedelta
from kafka import KafkaProducer
from kafka.errors import KafkaError
import requests
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import KAFKA_BROKER, KAFKA_TOPIC_CONSUMOS, NUM_CLIENTES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsumptionProducer:
    def __init__(self, bootstrap_servers=KAFKA_BROKER):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.api_url = "http://data-generator:8000"
        
    def connect(self):
        """Conecta al broker de Kafka"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',
                retries=3,
                max_in_flight_requests_per_connection=1
            )
            logger.info(f"✓ Conectado a Kafka: {self.bootstrap_servers}")
        except Exception as e:
            logger.error(f"✗ Error conectando a Kafka: {e}")
            raise
    
    def disconnect(self):
        """Desconecta de Kafka"""
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Desconectado de Kafka")
    
    def enviar_consumo_horario(self, consumo_horario: dict):
        """Envía un registro de consumo horario a Kafka"""
        try:
            self.producer.send(
                KAFKA_TOPIC_CONSUMOS,
                value=consumo_horario
            ).get(timeout=10)
            logger.debug(f"✓ Enviado: {consumo_horario['propietario_id']} - {consumo_horario['timestamp']}")
        except KafkaError as e:
            logger.error(f"✗ Error enviando a Kafka: {e}")
    
    def obtener_datos_api(self, num_clientes: int = NUM_CLIENTES):
        """Obtiene datos de la API de generación"""
        try:
            response = requests.post(
                f"{self.api_url}/generar/batch",
                params={"num_clientes": num_clientes, "num_sospechosos": max(1, int(num_clientes * 0.1))},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"✗ Error obteniendo datos de API: {e}")
            return None
    
    def producir_lote(self, num_clientes: int = NUM_CLIENTES, delay_entre_registros: float = 0.1):
        """Produce un lote de datos de consumo para múltiples clientes"""
        logger.info(f"📊 Generando datos para {num_clientes} clientes...")
        
        datos = self.obtener_datos_api(num_clientes)
        if not datos:
            logger.error("No se pudieron obtener datos de la API")
            return 0
        
        total_enviados = 0
        for cliente_resultado in datos['resultados']:
            cliente_id = cliente_resultado['cliente_id']
            es_sospechoso = cliente_resultado['es_sospechoso']
            
            for consumo in cliente_resultado['consumos']:
                consumo_dict = consumo.dict() if hasattr(consumo, 'dict') else consumo
                consumo_dict['timestamp_procesado'] = datetime.now().isoformat()
                consumo_dict['es_sospechoso'] = es_sospechoso
                
                self.enviar_consumo_horario(consumo_dict)
                total_enviados += 1
                time.sleep(delay_entre_registros)
        
        logger.info(f"✓ Enviados {total_enviados} registros de consumo")
        return total_enviados
    
    def producir_continuo(self, intervalo_minutos: int = 60, num_clientes: int = NUM_CLIENTES):
        """Produce datos continuamente simulando ingesta real"""
        logger.info(f"🔄 Iniciando ingesta continua (intervalo: {intervalo_minutos} min)")
        
        try:
            while True:
                logger.info(f"[{datetime.now()}] Iniciando ciclo de producción...")
                self.producir_lote(num_clientes)
                
                logger.info(f"Esperando {intervalo_minutos} minutos hasta el próximo ciclo...")
                time.sleep(intervalo_minutos * 60)
        
        except KeyboardInterrupt:
            logger.info("\n⏹️ Ingesta detenida por el usuario")
        except Exception as e:
            logger.error(f"Error en ciclo de producción: {e}")
        finally:
            self.disconnect()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Productor Kafka de consumos")
    parser.add_argument("--mode", choices=["once", "continuous"], default="once",
                       help="Modo: una sola vez o continuo")
    parser.add_argument("--clients", type=int, default=NUM_CLIENTES,
                       help=f"Número de clientes a generar (default: {NUM_CLIENTES})")
    parser.add_argument("--interval", type=int, default=60,
                       help="Intervalo entre ciclos en minutos (para modo continuo)")
    parser.add_argument("--broker", default=KAFKA_BROKER,
                       help=f"Broker de Kafka (default: {KAFKA_BROKER})")
    
    args = parser.parse_args()
    
    producer = ConsumptionProducer(bootstrap_servers=args.broker)
    producer.connect()
    
    try:
        if args.mode == "once":
            producer.producir_lote(args.clients)
        else:
            producer.producir_continuo(args.interval, args.clients)
    finally:
        producer.disconnect()

if __name__ == "__main__":
    main()
