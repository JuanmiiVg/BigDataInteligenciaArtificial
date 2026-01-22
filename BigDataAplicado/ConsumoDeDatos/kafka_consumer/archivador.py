"""
Sistema de Archivado y Limpieza de Datos
Mueve datos antiguos a históricos y libera espacio
"""
import sys
import os
import logging
from datetime import datetime, timedelta
import psycopg2
from pymongo import MongoClient
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    POSTGRES_URI, MONGO_URI, MONGO_DB, 
    COLLECTION_CONSUMOS_DIARIOS, COLLECTION_ANOMALIAS
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ArchivadorDatos:
    """Archiva y limpia datos antiguos de bases de datos"""
    
    def __init__(self):
        self.pg_conn = None
        self.pg_cursor = None
        self.mongo_client = None
        self.mongo_db = None
    
    def conectar(self):
        """Conecta a las bases de datos"""
        try:
            # PostgreSQL
            self.pg_conn = psycopg2.connect(POSTGRES_URI)
            self.pg_cursor = self.pg_conn.cursor()
            logger.info("✓ Conectado a PostgreSQL")
            
            # MongoDB
            self.mongo_client = MongoClient(MONGO_URI)
            self.mongo_db = self.mongo_client[MONGO_DB]
            logger.info("✓ Conectado a MongoDB")
            
            return True
        except Exception as e:
            logger.error(f"✗ Error conectando: {e}")
            return False
    
    def crear_tablas_archivo(self):
        """Crea tablas de archivo si no existen"""
        try:
            # Tabla de consumos archivados
            self.pg_cursor.execute("""
                CREATE TABLE IF NOT EXISTS consumos_diarios_archivo (
                    id SERIAL PRIMARY KEY,
                    propietario_id VARCHAR(50),
                    fecha DATE,
                    hora INT,
                    consumo_kwh NUMERIC(10, 3),
                    anomalia_detectada BOOLEAN,
                    score_anomalia NUMERIC(3, 3),
                    es_sospechoso BOOLEAN,
                    fecha_archivado TIMESTAMP DEFAULT NOW(),
                    CONSTRAINT check_hora CHECK (hora >= 0 AND hora <= 23)
                );
                
                CREATE INDEX IF NOT EXISTS idx_consumos_archivo_fecha 
                    ON consumos_diarios_archivo(fecha);
                CREATE INDEX IF NOT EXISTS idx_consumos_archivo_cliente 
                    ON consumos_diarios_archivo(propietario_id);
            """)
            
            # Tabla de registro de archivados
            self.pg_cursor.execute("""
                CREATE TABLE IF NOT EXISTS log_archivado (
                    id SERIAL PRIMARY KEY,
                    tabla_origen VARCHAR(100),
                    fecha_inicio DATE,
                    fecha_fin DATE,
                    registros_archivados INT,
                    timestamp TIMESTAMP DEFAULT NOW(),
                    estado VARCHAR(20)
                );
            """)
            
            self.pg_conn.commit()
            logger.info("✓ Tablas de archivo creadas/verificadas")
            
        except Exception as e:
            logger.error(f"✗ Error creando tablas: {e}")
            self.pg_conn.rollback()
    
    def crear_colecciones_archivo(self):
        """Crea colecciones de archivo en MongoDB"""
        try:
            # Verificar/crear colecciones
            colecciones = self.mongo_db.list_collection_names()
            
            if "anomalias_detectadas_archivo" not in colecciones:
                self.mongo_db.create_collection("anomalias_detectadas_archivo")
                logger.info("✓ Colección 'anomalias_detectadas_archivo' creada")
            
            if "log_archivado_mongo" not in colecciones:
                self.mongo_db.create_collection("log_archivado_mongo")
                logger.info("✓ Colección 'log_archivado_mongo' creada")
            
        except Exception as e:
            logger.error(f"✗ Error creando colecciones: {e}")
    
    def archivar_consumos_postgres(self, dias_antiguedad=90):
        """
        Archiva consumos diarios más antiguos de X días
        
        Args:
            dias_antiguedad: Días para considerar un registro como antiguo
        """
        try:
            fecha_limite = datetime.now() - timedelta(days=dias_antiguedad)
            fecha_str = fecha_limite.strftime('%Y-%m-%d')
            
            logger.info(f"🔄 Archivando consumos de PostgreSQL (antes de {fecha_str})...")
            
            # Copiar a tabla de archivo
            self.pg_cursor.execute(f"""
                INSERT INTO consumos_diarios_archivo 
                (propietario_id, fecha, hora, consumo_kwh, anomalia_detectada, 
                 score_anomalia, es_sospechoso)
                SELECT propietario_id, fecha, hora, consumo_kwh, anomalia_detectada,
                       score_anomalia, es_sospechoso
                FROM consumos_diarios
                WHERE fecha < %s::DATE
            """, (fecha_str,))
            
            registros_copiados = self.pg_cursor.rowcount
            
            if registros_copiados > 0:
                # Borrar del original
                self.pg_cursor.execute("""
                    DELETE FROM consumos_diarios WHERE fecha < %s::DATE
                """, (fecha_str,))
                
                registros_borrados = self.pg_cursor.rowcount
                
                # Registrar en log
                self.pg_cursor.execute("""
                    INSERT INTO log_archivado 
                    (tabla_origen, fecha_inicio, fecha_fin, registros_archivados, estado)
                    SELECT 'consumos_diarios', 
                           (SELECT MIN(fecha) FROM consumos_diarios_archivo),
                           %s::DATE,
                           %s,
                           'exitoso'
                """, (fecha_str, registros_borrados))
                
                self.pg_conn.commit()
                
                logger.info(f"✓ Archivados {registros_copiados} registros")
                logger.info(f"✓ Borrados {registros_borrados} registros de tabla activa")
                
                return registros_borrados
            else:
                logger.info("⚠️ No hay registros antiguos para archivar")
                return 0
                
        except Exception as e:
            logger.error(f"✗ Error archivando PostgreSQL: {e}")
            self.pg_conn.rollback()
            return 0
    
    def archivar_anomalias_mongodb(self, dias_antiguedad=90):
        """
        Archiva anomalías detectadas más antiguas de X días
        
        Args:
            dias_antiguedad: Días para considerar un registro como antiguo
        """
        try:
            fecha_limite = datetime.now() - timedelta(days=dias_antiguedad)
            
            logger.info(f"🔄 Archivando anomalías de MongoDB (antes de {dias_antiguedad} días)...")
            
            coll_activa = self.mongo_db[COLLECTION_ANOMALIAS]
            coll_archivo = self.mongo_db["anomalias_detectadas_archivo"]
            coll_log = self.mongo_db["log_archivado_mongo"]
            
            # Buscar documentos antiguos
            documentos_antiguos = list(coll_activa.find({
                'timestamp': {'$lt': fecha_limite.isoformat()}
            }))
            
            if documentos_antiguos:
                # Copiar a colección de archivo
                if len(documentos_antiguos) > 0:
                    coll_archivo.insert_many(documentos_antiguos)
                    logger.info(f"✓ Copiados {len(documentos_antiguos)} documentos a archivo")
                
                # Borrar de colección activa
                resultado = coll_activa.delete_many({
                    'timestamp': {'$lt': fecha_limite.isoformat()}
                })
                
                logger.info(f"✓ Borrados {resultado.deleted_count} documentos de tabla activa")
                
                # Registrar en log
                coll_log.insert_one({
                    'coleccion_origen': COLLECTION_ANOMALIAS,
                    'fecha_limite': fecha_limite.isoformat(),
                    'documentos_archivados': len(documentos_antiguos),
                    'documentos_borrados': resultado.deleted_count,
                    'timestamp': datetime.now().isoformat(),
                    'estado': 'exitoso'
                })
                
                return resultado.deleted_count
            else:
                logger.info("⚠️ No hay documentos antiguos para archivar")
                return 0
                
        except Exception as e:
            logger.error(f"✗ Error archivando MongoDB: {e}")
            return 0
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas de almacenamiento"""
        try:
            # PostgreSQL
            self.pg_cursor.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM consumos_diarios) as registros_activos,
                    (SELECT COUNT(*) FROM consumos_diarios_archivo) as registros_archivados,
                    (SELECT COUNT(*) FROM log_archivado) as operaciones_archivado
            """)
            
            pg_stats = self.pg_cursor.fetchone()
            
            # MongoDB
            stats_activas = self.mongo_db[COLLECTION_ANOMALIAS].count_documents({})
            stats_archivo = self.mongo_db["anomalias_detectadas_archivo"].count_documents({})
            
            return {
                'postgresql': {
                    'registros_activos': pg_stats[0],
                    'registros_archivados': pg_stats[1],
                    'operaciones_archivado': pg_stats[2]
                },
                'mongodb': {
                    'anomalias_activas': stats_activas,
                    'anomalias_archivadas': stats_archivo
                }
            }
            
        except Exception as e:
            logger.error(f"✗ Error obteniendo estadísticas: {e}")
            return None
    
    def generar_reporte(self):
        """Genera reporte de archivado"""
        try:
            logger.info("\n" + "=" * 70)
            logger.info("📊 REPORTE DE ALMACENAMIENTO")
            logger.info("=" * 70)
            
            stats = self.obtener_estadisticas()
            
            if stats:
                logger.info("\n📂 PostgreSQL:")
                logger.info(f"  Registros Activos: {stats['postgresql']['registros_activos']:,}")
                logger.info(f"  Registros Archivados: {stats['postgresql']['registros_archivados']:,}")
                logger.info(f"  Operaciones: {stats['postgresql']['operaciones_archivado']}")
                
                logger.info("\n📂 MongoDB:")
                logger.info(f"  Anomalías Activas: {stats['mongodb']['anomalias_activas']:,}")
                logger.info(f"  Anomalías Archivadas: {stats['mongodb']['anomalias_archivadas']:,}")
                
                # Calcular reducción de almacenamiento
                total_antes = (stats['postgresql']['registros_activos'] + 
                             stats['postgresql']['registros_archivados'])
                if total_antes > 0:
                    reduccion = (stats['postgresql']['registros_archivados'] / total_antes) * 100
                    logger.info(f"\n💾 Reducción de datos activos: {reduccion:.1f}%")
            
            logger.info("=" * 70 + "\n")
            
        except Exception as e:
            logger.error(f"✗ Error generando reporte: {e}")
    
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
    """Ejecutar archivado"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Archivador de datos del sistema ConsumoDeDatos')
    parser.add_argument('--dias', type=int, default=30, 
                       help='Días de antiguedad para archivar datos DIARIOS (default: 30 - menos críticos)')
    parser.add_argument('--solo-postgres', action='store_true',
                       help='Archivar solo PostgreSQL (consumos_diarios)')
    parser.add_argument('--solo-mongodb', action='store_true',
                       help='Archivar solo MongoDB (anomalias_detectadas)')
    parser.add_argument('--reporte', action='store_true',
                       help='Solo mostrar reporte sin archivar')
    parser.add_argument('--agresivo', action='store_true',
                       help='Modo agresivo: archivar datos de solo 7 días (libera mucho espacio)')
    
    args = parser.parse_args()
    
    # Modo agresivo: archiva datos de 7 días (menos críticos)
    if args.agresivo:
        args.dias = 7
        logger.warning("⚠️ MODO AGRESIVO ACTIVADO - Archivará datos de más de 7 días")
    
    archivador = ArchivadorDatos()
    
    if not archivador.conectar():
        sys.exit(1)
    
    # Crear estructuras de archivo
    archivador.crear_tablas_archivo()
    archivador.crear_colecciones_archivo()
    
    if args.reporte:
        # Solo mostrar reporte
        archivador.generar_reporte()
    else:
        # Archivar datos
        logger.info("\n" + "=" * 70)
        logger.info("🔄 INICIANDO ARCHIVADO DE DATOS")
        logger.info(f"📌 Datos Diarios: se archivarán registros de más de {args.dias} días")
        logger.info("📌 Datos Mensuales: se conservan SIEMPRE (son críticos)")
        logger.info("=" * 70 + "\n")
        
        total_archivado = 0
        
        # PostgreSQL: datos diarios MENOS críticos
        if not args.solo_mongodb:
            logger.info("💡 Archivando consumos_diarios (menos críticos, tenemos mensuales)...")
            total_archivado += archivador.archivar_consumos_postgres(args.dias)
        
        # MongoDB: anomalías
        if not args.solo_postgres:
            logger.info("💡 Archivando anomalías (para mantener activo limpio)...")
            total_archivado += archivador.archivar_anomalias_mongodb(args.dias)
        
        logger.info(f"\n✓ Total de registros procesados: {total_archivado:,}\n")
        logger.info("✅ Datos mensuales (consumos_mensuales) permanecen sin cambios\n")
        
        # Mostrar reporte final
        archivador.generar_reporte()
    
    archivador.desconectar()
