"""
Sistema de Restauración de Datos Archivados
Permite restaurar datos desde el archivo si es necesario
"""
import sys
import os
import logging
from datetime import datetime
import psycopg2
from pymongo import MongoClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    POSTGRES_URI, MONGO_URI, MONGO_DB,
    COLLECTION_ANOMALIAS
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RestauradorDatos:
    """Restaura datos desde archivo si es necesario"""
    
    def __init__(self):
        self.pg_conn = None
        self.pg_cursor = None
        self.mongo_client = None
        self.mongo_db = None
    
    def conectar(self):
        """Conecta a las bases de datos"""
        try:
            self.pg_conn = psycopg2.connect(POSTGRES_URI)
            self.pg_cursor = self.pg_conn.cursor()
            logger.info("✓ Conectado a PostgreSQL")
            
            self.mongo_client = MongoClient(MONGO_URI)
            self.mongo_db = self.mongo_client[MONGO_DB]
            logger.info("✓ Conectado a MongoDB")
            
            return True
        except Exception as e:
            logger.error(f"✗ Error conectando: {e}")
            return False
    
    def restaurar_consumos_postgres(self, fecha_inicio=None, fecha_fin=None):
        """
        Restaura consumos diarios desde archivo
        
        Args:
            fecha_inicio: Fecha inicial YYYY-MM-DD
            fecha_fin: Fecha final YYYY-MM-DD
        """
        try:
            logger.info("🔄 Restaurando consumos desde archivo...")
            
            if not fecha_inicio or not fecha_fin:
                # Restaurar todo
                query = """
                    INSERT INTO consumos_diarios 
                    (propietario_id, fecha, hora, consumo_kwh, anomalia_detectada, 
                     score_anomalia, es_sospechoso)
                    SELECT propietario_id, fecha, hora, consumo_kwh, anomalia_detectada,
                           score_anomalia, es_sospechoso
                    FROM consumos_diarios_archivo
                """
                self.pg_cursor.execute(query)
            else:
                # Restaurar rango específico
                query = """
                    INSERT INTO consumos_diarios 
                    (propietario_id, fecha, hora, consumo_kwh, anomalia_detectada, 
                     score_anomalia, es_sospechoso)
                    SELECT propietario_id, fecha, hora, consumo_kwh, anomalia_detectada,
                           score_anomalia, es_sospechoso
                    FROM consumos_diarios_archivo
                    WHERE fecha BETWEEN %s::DATE AND %s::DATE
                """
                self.pg_cursor.execute(query, (fecha_inicio, fecha_fin))
            
            registros_restaurados = self.pg_cursor.rowcount
            self.pg_conn.commit()
            
            logger.info(f"✓ Restaurados {registros_restaurados:,} registros")
            return registros_restaurados
            
        except Exception as e:
            logger.error(f"✗ Error restaurando PostgreSQL: {e}")
            self.pg_conn.rollback()
            return 0
    
    def restaurar_anomalias_mongodb(self, fecha_inicio=None):
        """
        Restaura anomalías detectadas desde archivo
        
        Args:
            fecha_inicio: Fecha inicial ISO (restaura desde esta fecha)
        """
        try:
            logger.info("🔄 Restaurando anomalías desde archivo...")
            
            coll_activa = self.mongo_db[COLLECTION_ANOMALIAS]
            coll_archivo = self.mongo_db["anomalias_detectadas_archivo"]
            
            if not fecha_inicio:
                # Restaurar todo
                documentos = list(coll_archivo.find({}))
            else:
                # Restaurar desde fecha específica
                documentos = list(coll_archivo.find({
                    'timestamp': {'$gte': fecha_inicio}
                }))
            
            if documentos:
                # Insertar en colección activa
                coll_activa.insert_many(documentos)
                logger.info(f"✓ Restaurados {len(documentos):,} documentos")
                return len(documentos)
            else:
                logger.info("⚠️ No hay documentos para restaurar")
                return 0
                
        except Exception as e:
            logger.error(f"✗ Error restaurando MongoDB: {e}")
            return 0
    
    def listar_archivos(self):
        """Lista archivos disponibles para restaurar"""
        try:
            logger.info("\n📋 ARCHIVOS DISPONIBLES PARA RESTAURAR")
            logger.info("=" * 70)
            
            # PostgreSQL
            self.pg_cursor.execute("""
                SELECT fecha_inicio, fecha_fin, registros_archivados, timestamp
                FROM log_archivado
                ORDER BY timestamp DESC
                LIMIT 10
            """)
            
            resultados_pg = self.pg_cursor.fetchall()
            
            if resultados_pg:
                logger.info("\n📂 PostgreSQL (consumos_diarios):")
                for row in resultados_pg:
                    logger.info(f"  {row[0]} a {row[1]} - {row[2]:,} registros ({row[3]})")
            
            # MongoDB
            coll_log = self.mongo_db["log_archivado_mongo"]
            logs_mongo = list(coll_log.find({}).sort('timestamp', -1).limit(10))
            
            if logs_mongo:
                logger.info("\n📂 MongoDB (anomalias_detectadas):")
                for log in logs_mongo:
                    logger.info(f"  Antes de {log['fecha_limite']} - "
                              f"{log['documentos_archivados']:,} documentos "
                              f"({log['timestamp']})")
            
            logger.info("=" * 70 + "\n")
            
        except Exception as e:
            logger.error(f"✗ Error listando archivos: {e}")
    
    def eliminar_permanentemente(self, dias_archivo=365):
        """
        Elimina datos archivados de forma permanente
        (No se puede recuperar después)
        
        Args:
            dias_archivo: Solo elimina datos archivados hace más de X días
        """
        try:
            logger.warning("\n⚠️ ADVERTENCIA: Esta acción eliminará datos de forma permanente")
            confirmar = input("¿Está seguro? (escriba 'SÍ' para confirmar): ")
            
            if confirmar.upper() != 'SÍ':
                logger.info("Operación cancelada")
                return
            
            from datetime import datetime, timedelta
            fecha_limite = datetime.now() - timedelta(days=dias_archivo)
            
            logger.info(f"🗑️ Eliminando permanentemente datos archivados antes de {fecha_limite.date()}...")
            
            # PostgreSQL
            self.pg_cursor.execute("""
                DELETE FROM consumos_diarios_archivo 
                WHERE fecha_archivado < %s::TIMESTAMP
            """, (fecha_limite.isoformat(),))
            
            registros_eliminados = self.pg_cursor.rowcount
            self.pg_conn.commit()
            
            logger.info(f"✓ Eliminados {registros_eliminados:,} registros de PostgreSQL")
            
            # MongoDB
            coll_archivo = self.mongo_db["anomalias_detectadas_archivo"]
            resultado = coll_archivo.delete_many({
                'timestamp': {'$lt': fecha_limite.isoformat()}
            })
            
            logger.info(f"✓ Eliminados {resultado.deleted_count:,} documentos de MongoDB")
            
        except Exception as e:
            logger.error(f"✗ Error eliminando: {e}")
            self.pg_conn.rollback()
    
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
    import argparse
    
    parser = argparse.ArgumentParser(description='Restaurador de datos archivados')
    parser.add_argument('--listar', action='store_true',
                       help='Listar archivos disponibles')
    parser.add_argument('--restaurar-todos', action='store_true',
                       help='Restaurar todos los datos archivados')
    parser.add_argument('--restaurar-desde', type=str,
                       help='Restaurar consumos desde fecha (YYYY-MM-DD)')
    parser.add_argument('--restaurar-hasta', type=str,
                       help='Restaurar consumos hasta fecha (YYYY-MM-DD)')
    parser.add_argument('--solo-postgresql', action='store_true',
                       help='Solo restaurar PostgreSQL')
    parser.add_argument('--solo-mongodb', action='store_true',
                       help='Solo restaurar MongoDB')
    parser.add_argument('--eliminar-permanente', action='store_true',
                       help='Eliminar datos archivados de forma permanente')
    parser.add_argument('--dias-archivo', type=int, default=365,
                       help='Días de archivado antes de eliminar permanentemente')
    
    args = parser.parse_args()
    
    restaurador = RestauradorDatos()
    
    if not restaurador.conectar():
        sys.exit(1)
    
    if args.listar:
        restaurador.listar_archivos()
    elif args.eliminar_permanente:
        restaurador.eliminar_permanentemente(args.dias_archivo)
    elif args.restaurar_todos:
        logger.info("\n" + "=" * 70)
        logger.info("🔄 RESTAURANDO TODOS LOS DATOS")
        logger.info("=" * 70 + "\n")
        
        if not args.solo_mongodb:
            restaurador.restaurar_consumos_postgres()
        if not args.solo_postgresql:
            restaurador.restaurar_anomalias_mongodb()
        
        logger.info("\n✓ Restauración completada\n")
    elif args.restaurar_desde and args.restaurar_hasta:
        logger.info("\n" + "=" * 70)
        logger.info(f"🔄 RESTAURANDO DATOS: {args.restaurar_desde} a {args.restaurar_hasta}")
        logger.info("=" * 70 + "\n")
        
        restaurador.restaurar_consumos_postgres(args.restaurar_desde, args.restaurar_hasta)
        logger.info("\n✓ Restauración completada\n")
    else:
        restaurador.listar_archivos()
    
    restaurador.desconectar()
