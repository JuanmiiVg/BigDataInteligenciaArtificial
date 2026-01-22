"""
Módulo para interactuar con PostgreSQL - Almacenamiento de consumos diarios
"""
import sys
import os
import logging
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_batch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import POSTGRES_URI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostgresDataStore:
    """Almacena consumos diarios en PostgreSQL"""
    
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def conectar(self):
        """Conecta a PostgreSQL"""
        try:
            self.conn = psycopg2.connect(POSTGRES_URI)
            self.cursor = self.conn.cursor()
            self._crear_tablas()
            logger.info("✓ Conectado a PostgreSQL")
        except Exception as e:
            logger.error(f"✗ Error conectando a PostgreSQL: {e}")
            raise
    
    def _crear_tablas(self):
        """Crea tablas si no existen"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS consumos_diarios (
                    id SERIAL PRIMARY KEY,
                    propietario_id VARCHAR(50) NOT NULL,
                    fecha DATE NOT NULL,
                    hora INT NOT NULL,
                    consumo_kwh FLOAT NOT NULL,
                    anomalia_detectada BOOLEAN DEFAULT FALSE,
                    score_anomalia FLOAT DEFAULT 0.0,
                    severidad VARCHAR(20),
                    tipos_anomalia TEXT[],
                    es_sospechoso BOOLEAN DEFAULT FALSE,
                    timestamp_consumo TIMESTAMP NOT NULL,
                    timestamp_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(propietario_id, fecha, hora)
                );
                
                CREATE INDEX IF NOT EXISTS idx_propietario_fecha 
                ON consumos_diarios(propietario_id, fecha);
                
                CREATE INDEX IF NOT EXISTS idx_fecha 
                ON consumos_diarios(fecha);
            """)
            self.conn.commit()
            logger.info("✓ Tablas creadas/verificadas")
        except Exception as e:
            logger.error(f"✗ Error creando tablas: {e}")
            self.conn.rollback()
    
    def guardar_consumo(self, consumo_data: dict):
        """Guarda un consumo en PostgreSQL"""
        try:
            query = """
                INSERT INTO consumos_diarios 
                (propietario_id, fecha, hora, consumo_kwh, anomalia_detectada, 
                 score_anomalia, severidad, tipos_anomalia, es_sospechoso, 
                 timestamp_consumo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (propietario_id, fecha, hora) 
                DO UPDATE SET
                    consumo_kwh = EXCLUDED.consumo_kwh,
                    anomalia_detectada = EXCLUDED.anomalia_detectada,
                    score_anomalia = EXCLUDED.score_anomalia,
                    severidad = EXCLUDED.severidad,
                    tipos_anomalia = EXCLUDED.tipos_anomalia,
                    es_sospechoso = EXCLUDED.es_sospechoso,
                    timestamp_registro = CURRENT_TIMESTAMP
            """
            
            fecha = datetime.fromisoformat(consumo_data['timestamp']).date()
            self.cursor.execute(query, (
                consumo_data['propietario_id'],
                fecha,
                consumo_data['hora'],
                consumo_data['consumo_kwh'],
                consumo_data.get('anomalia_detectada', False),
                consumo_data.get('score_anomalia', 0.0),
                consumo_data.get('severidad', 'normal'),
                consumo_data.get('tipos_anomalia', []),
                consumo_data.get('es_sospechoso', False),
                consumo_data['timestamp']
            ))
            self.conn.commit()
            
        except Exception as e:
            logger.error(f"✗ Error guardando consumo: {e}")
            self.conn.rollback()
    
    def guardar_lote(self, consumos: list):
        """Guarda un lote de consumos"""
        try:
            query = """
                INSERT INTO consumos_diarios 
                (propietario_id, fecha, hora, consumo_kwh, anomalia_detectada, 
                 score_anomalia, severidad, tipos_anomalia, es_sospechoso, 
                 timestamp_consumo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (propietario_id, fecha, hora) 
                DO UPDATE SET
                    consumo_kwh = EXCLUDED.consumo_kwh,
                    anomalia_detectada = EXCLUDED.anomalia_detectada,
                    score_anomalia = EXCLUDED.score_anomalia,
                    severidad = EXCLUDED.severidad,
                    tipos_anomalia = EXCLUDED.tipos_anomalia,
                    es_sospechoso = EXCLUDED.es_sospechoso,
                    timestamp_registro = CURRENT_TIMESTAMP
            """
            
            datos = []
            for consumo in consumos:
                fecha = datetime.fromisoformat(consumo['timestamp']).date()
                datos.append((
                    consumo['propietario_id'],
                    fecha,
                    consumo['hora'],
                    consumo['consumo_kwh'],
                    consumo.get('anomalia_detectada', False),
                    consumo.get('score_anomalia', 0.0),
                    consumo.get('severidad', 'normal'),
                    consumo.get('tipos_anomalia', []),
                    consumo.get('es_sospechoso', False),
                    consumo['timestamp']
                ))
            
            execute_batch(self.cursor, query, datos, page_size=1000)
            self.conn.commit()
            logger.debug(f"✓ Guardados {len(datos)} registros")
            
        except Exception as e:
            logger.error(f"✗ Error guardando lote: {e}")
            self.conn.rollback()
    
    def desconectar(self):
        """Cierra la conexión"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            logger.info("Desconectado de PostgreSQL")
