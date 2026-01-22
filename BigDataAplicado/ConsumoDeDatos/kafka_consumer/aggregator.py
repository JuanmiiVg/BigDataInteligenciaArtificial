"""
Script de agregación: Consolida consumos diarios (PostgreSQL) en mensuales (MongoDB)
Se ejecuta diariamente para crear resúmenes mensuales en MongoDB
"""
import sys
import os
import logging
from datetime import datetime, timedelta
import psycopg2
from pymongo import MongoClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    POSTGRES_URI, MONGO_URI, MONGO_DB, 
    COLLECTION_CONSUMOS_MENSUALES
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgregadorDatos:
    """Agrega consumos diarios en resúmenes mensuales"""
    
    def __init__(self):
        self.pg_conn = None
        self.pg_cursor = None
        self.mongo_client = None
        self.mongo_db = None
    
    def conectar(self):
        """Conecta a ambas bases de datos"""
        try:
            # PostgreSQL
            self.pg_conn = psycopg2.connect(POSTGRES_URI)
            self.pg_cursor = self.pg_conn.cursor()
            logger.info("✓ Conectado a PostgreSQL")
            
            # MongoDB
            self.mongo_client = MongoClient(MONGO_URI)
            self.mongo_db = self.mongo_client[MONGO_DB]
            logger.info("✓ Conectado a MongoDB")
        except Exception as e:
            logger.error(f"✗ Error conectando: {e}")
            raise
    
    def agregar_mes(self, propietario_id: str = None, mes: str = None):
        """
        Agrega consumos de un mes completo
        Si mes es None, usa el mes anterior
        Formato mes: 'YYYY-MM'
        """
        if mes is None:
            # Mes anterior
            hoy = datetime.now()
            primer_dia = hoy.replace(day=1)
            ultimo_dia_mes_anterior = primer_dia - timedelta(days=1)
            mes = ultimo_dia_mes_anterior.strftime('%Y-%m')
        
        logger.info(f"🔄 Agregando datos de {mes}...")
        
        try:
            year, month = mes.split('-')
            
            # Obtener consumos diarios del mes en PostgreSQL
            query = """
                SELECT 
                    propietario_id,
                    DATE_TRUNC('month', fecha)::DATE as mes,
                    COUNT(*) as num_registros,
                    SUM(consumo_kwh) as consumo_total,
                    AVG(consumo_kwh) as consumo_promedio,
                    MIN(consumo_kwh) as consumo_minimo,
                    MAX(consumo_kwh) as consumo_maximo,
                    STDDEV(consumo_kwh) as consumo_desviacion,
                    COUNT(CASE WHEN anomalia_detectada THEN 1 END) as anomalias_detectadas,
                    COUNT(CASE WHEN severidad = 'crítica' THEN 1 END) as anomalias_criticas,
                    COUNT(CASE WHEN severidad = 'alta' THEN 1 END) as anomalias_altas,
                    COUNT(CASE WHEN severidad = 'media' THEN 1 END) as anomalias_medias,
                    MAX(score_anomalia) as max_score_anomalia,
                    AVG(score_anomalia) as avg_score_anomalia,
                    (SUM(CASE WHEN hora IN (0,1,2,3,4,5,23) THEN consumo_kwh ELSE 0 END) / 
                     NULLIF(COUNT(CASE WHEN hora IN (0,1,2,3,4,5,23) THEN 1 END), 0)) as consumo_noche_promedio,
                    (SUM(CASE WHEN hora IN (18,19,20,21,22) THEN consumo_kwh ELSE 0 END) / 
                     NULLIF(COUNT(CASE WHEN hora IN (18,19,20,21,22) THEN 1 END), 0)) as consumo_punta_promedio,
                    BOOL_OR(es_sospechoso) as tiene_comportamiento_sospechoso
                FROM consumos_diarios
                WHERE EXTRACT(YEAR FROM fecha) = %s::INT 
                  AND EXTRACT(MONTH FROM fecha) = %s::INT
            """
            
            if propietario_id:
                query += f" AND propietario_id = %s"
                self.pg_cursor.execute(query + " GROUP BY propietario_id, mes", 
                                      (year, month, propietario_id))
            else:
                query += " GROUP BY propietario_id, mes"
                self.pg_cursor.execute(query, (year, month))
            
            resultados = self.pg_cursor.fetchall()
            
            if not resultados:
                logger.info(f"⚠️ No hay datos para {mes}")
                return 0
            
            # Insertar en MongoDB
            coll = self.mongo_db[COLLECTION_CONSUMOS_MENSUALES]
            
            insertar = 0
            for row in resultados:
                documento = {
                    '_id': f"{row[0]}_{mes}",  # propietario_id_YYYY-MM
                    'propietario_id': row[0],
                    'mes': row[1].isoformat() if row[1] else mes,  # Convertir date a string
                    'mes_str': mes,
                    'num_registros': int(row[2]),
                    'consumo_total': round(float(row[3]) if row[3] else 0, 3),
                    'consumo_promedio': round(float(row[4]) if row[4] else 0, 3),
                    'consumo_minimo': round(float(row[5]) if row[5] else 0, 3),
                    'consumo_maximo': round(float(row[6]) if row[6] else 0, 3),
                    'consumo_desviacion': round(float(row[7]) if row[7] else 0, 3),
                    'anomalias_detectadas': int(row[8]),
                    'anomalias_criticas': int(row[9]),
                    'anomalias_altas': int(row[10]),
                    'anomalias_medias': int(row[11]),
                    'max_score_anomalia': round(float(row[12]) if row[12] else 0, 3),
                    'avg_score_anomalia': round(float(row[13]) if row[13] else 0, 3),
                    'consumo_noche_promedio': round(float(row[14]) if row[14] else 0, 3),
                    'consumo_punta_promedio': round(float(row[15]) if row[15] else 0, 3),
                    'tiene_comportamiento_sospechoso': bool(row[16]),
                    'timestamp': datetime.now().isoformat()
                }
                
                coll.replace_one({'_id': documento['_id']}, documento, upsert=True)
                insertar += 1
            
            logger.info(f"✓ Agregados {insertar} resúmenes mensuales para {mes}")
            return insertar
            
        except Exception as e:
            logger.error(f"✗ Error en agregación: {e}")
            return 0
    
    def agregar_ultimo_mes_completo(self):
        """Agrega el mes anterior completo (útil para ejecución automática)"""
        hoy = datetime.now()
        primer_dia = hoy.replace(day=1)
        ultimo_dia_mes_anterior = primer_dia - timedelta(days=1)
        mes = ultimo_dia_mes_anterior.strftime('%Y-%m')
        
        return self.agregar_mes(mes=mes)
    
    def desconectar(self):
        """Cierra las conexiones"""
        if self.pg_cursor:
            self.pg_cursor.close()
        if self.pg_conn:
            self.pg_conn.close()
            logger.info("Desconectado de PostgreSQL")
        
        if self.mongo_client:
            self.mongo_client.close()
            logger.info("Desconectado de MongoDB")


if __name__ == "__main__":
    """Ejecutar agregación"""
    agregador = AgregadorDatos()
    agregador.conectar()
    
    # Si se proporciona un mes en argumentos, usarlo. Si no, usar mes anterior
    if len(sys.argv) > 1:
        mes = sys.argv[1]  # Formato: 2026-01
        agregador.agregar_mes(mes=mes)
    else:
        agregador.agregar_ultimo_mes_completo()
    
    agregador.desconectar()
