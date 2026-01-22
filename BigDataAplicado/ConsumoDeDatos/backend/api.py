"""
API Backend REST para consultar datos de consumos y anomalías
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    MONGO_URI, MONGO_DB, COLLECTION_CONSUMOS, COLLECTION_ANOMALIAS,
    COLLECTION_CONSUMOS_DIARIOS, API_HOST, API_PORT
)

try:
    from pymongo import MongoClient, DESCENDING, ASCENDING
except ImportError:
    logging.error("pymongo no instalado")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== FASTAPI ==========
app = FastAPI(
    title="Consumo Monitoring API",
    description="API para monitoreo y análisis de consumos en tiempo real",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== MODELOS ==========
class ConsumoResponse(BaseModel):
    propietario_id: str
    timestamp: str
    hora: int
    consumo_kwh: float
    anomalia_detectada: bool
    tipos_anomalia: List[str]
    score_anomalia: float
    severidad: str

class AnomaliaResponse(BaseModel):
    propietario_id: str
    timestamp_consumo: str
    timestamp_deteccion: str
    consumo_kwh: float
    hora: int
    tipos_anomalia: List[str]
    score_anomalia: float
    severidad: str
    es_sospechoso_cliente: bool

class EstadisticasCliente(BaseModel):
    propietario_id: str
    consumo_promedio_24h: float
    consumo_minimo: float
    consumo_maximo: float
    consumo_noche_promedio: float
    anomalias_detectadas: int
    anomalias_criticas: int
    es_cliente_sospechoso: bool

class ResumenAnomalia(BaseModel):
    total_anomalias: int
    anomalias_criticas: int
    anomalias_altas: int
    anomalias_medias: int
    clientes_afectados: int
    tipos_mas_frecuentes: List[str]

# ========== CONEXIÓN A MONGO ==========
mongo_client = None
db = None

def conectar_mongodb():
    global mongo_client, db
    import time
    max_retries = 10
    for intento in range(max_retries):
        try:
            mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
            mongo_client.server_info()
            db = mongo_client[MONGO_DB]
            logger.info(f"✓ MongoDB conectado (intento {intento + 1})")
            return True
        except Exception as e:
            logger.warning(f"Intento {intento + 1}/{max_retries} - Error conectando a MongoDB: {e}")
            if intento < max_retries - 1:
                espera = min(2 ** intento, 30)
                logger.info(f"Reintentando en {espera} segundos...")
                time.sleep(espera)
            else:
                logger.error(f"✗ No se pudo conectar a MongoDB después de {max_retries} intentos")
                raise

# ========== STARTUP ==========
# Intentar conectar a MongoDB al iniciar
try:
    conectar_mongodb()
except Exception as e:
    logger.error(f"Error en startup: {e}")
    # No salir, intentar nuevamente en el primer endpoint

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {"message": "Consumo Monitoring API", "version": "1.0.0"}

import atexit
def shutdown_hook():
    global mongo_client
    if mongo_client:
        mongo_client.close()
        logger.info("MongoDB desconectado")

atexit.register(shutdown_hook)

# ========== HEALTH CHECK ==========
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "consumo_backend",
        "timestamp": datetime.now().isoformat()
    }

def get_db():
    """Obtiene la base de datos, conectando si es necesario"""
    global db
    if db is None:
        conectar_mongodb()
    return db

# ========== ENDPOINTS: CONSUMOS ==========
@app.get("/api/consumos/últimas24h/{propietario_id}", response_model=List[ConsumoResponse])
async def obtener_consumos_24h(propietario_id: str):
    """Obtiene últimas 24 horas de consumos de un cliente"""
    try:
        db = get_db()
        hace_24h = datetime.now() - timedelta(hours=24)
        
        coll = db[COLLECTION_CONSUMOS]
        consumos = list(coll.find(
            {
                'propietario_id': propietario_id,
                'timestamp': {'$gte': hace_24h.isoformat()}
            },
            sort=[('timestamp', DESCENDING)]
        ).limit(100))
        
        if not consumos:
            raise HTTPException(status_code=404, detail="No se encontraron consumos")
        
        return [
            ConsumoResponse(
                propietario_id=c['propietario_id'],
                timestamp=c['timestamp'],
                hora=c['hora'],
                consumo_kwh=c['consumo_kwh'],
                anomalia_detectada=c.get('anomalia_detectada', False),
                tipos_anomalia=c.get('tipos_anomalia', []),
                score_anomalia=c.get('score_anomalia', 0),
                severidad=c.get('severidad', 'normal')
            )
            for c in consumos
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo consumos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/consumos/rango", response_model=List[ConsumoResponse])
async def obtener_consumos_rango(
    propietario_id: str,
    fecha_inicio: str,
    fecha_fin: str
):
    """Obtiene consumos en un rango de fechas"""
    try:
        db = get_db()
        f_inicio = datetime.fromisoformat(fecha_inicio)
        f_fin = datetime.fromisoformat(fecha_fin)
        
        coll = db[COLLECTION_CONSUMOS]
        consumos = list(coll.find(
            {
                'propietario_id': propietario_id,
                'timestamp': {
                    '$gte': f_inicio.isoformat(),
                    '$lte': f_fin.isoformat()
                }
            },
            sort=[('timestamp', ASCENDING)]
        ))
        
        return [
            ConsumoResponse(**c)
            for c in consumos
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Fechas inválidas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========== ENDPOINTS: ANOMALÍAS ==========
@app.get("/api/anomalias/últimas", response_model=List[AnomaliaResponse])
async def obtener_anomalias_recientes(
    limit: int = Query(50, le=1000),
    severidad: Optional[str] = None
):
    """Obtiene anomalías detectadas recientemente"""
    try:
        db = get_db()
        coll = db[COLLECTION_ANOMALIAS]
        filtro = {}
        
        if severidad:
            filtro['severidad'] = severidad
        
        anomalias = list(coll.find(
            filtro,
            sort=[('timestamp_deteccion', DESCENDING)]
        ).limit(limit))
        
        return [
            AnomaliaResponse(
                propietario_id=a['propietario_id'],
                timestamp_consumo=a['timestamp_consumo'],
                timestamp_deteccion=a['timestamp_deteccion'],
                consumo_kwh=a['consumo_kwh'],
                hora=a['hora'],
                tipos_anomalia=a.get('tipos_anomalia', []),
                score_anomalia=a.get('score_anomalia', 0),
                severidad=a.get('severidad', 'desconocida'),
                es_sospechoso_cliente=a.get('es_sospechoso_cliente', False)
            )
            for a in anomalias
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/anomalias/cliente/{propietario_id}", response_model=List[AnomaliaResponse])
async def obtener_anomalias_cliente(
    propietario_id: str,
    dias: int = Query(7, ge=1, le=90)
):
    """Obtiene anomalías de un cliente en los últimos N días"""
    try:
        hace_x_dias = datetime.now() - timedelta(days=dias)
        
        db = get_db()
        coll = db[COLLECTION_ANOMALIAS]
        anomalias = list(coll.find(
            {
                'propietario_id': propietario_id,
                'timestamp_deteccion': {'$gte': hace_x_dias.isoformat()}
            },
            sort=[('timestamp_deteccion', DESCENDING)]
        ))
        
        return [
            AnomaliaResponse(**a)
            for a in anomalias
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/anomalias/críticas", response_model=List[AnomaliaResponse])
async def obtener_anomalias_criticas():
    """Obtiene solo anomalías críticas de las últimas 24 horas"""
    try:
        hace_24h = datetime.now() - timedelta(hours=24)
        
        db = get_db()
        coll = db[COLLECTION_ANOMALIAS]
        anomalias = list(coll.find(
            {
                'severidad': 'crítica',
                'timestamp_deteccion': {'$gte': hace_24h.isoformat()}
            },
            sort=[('score_anomalia', DESCENDING)]
        ).limit(100))
        
        return [
            AnomaliaResponse(**a)
            for a in anomalias
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========== ENDPOINTS: ESTADÍSTICAS ==========
@app.get("/api/estadisticas/cliente/{propietario_id}", response_model=EstadisticasCliente)
async def obtener_estadisticas_cliente(propietario_id: str):
    """Obtiene estadísticas completas de un cliente"""
    try:
        coll_consumos = db[COLLECTION_CONSUMOS]
        coll_anomalias = db[COLLECTION_ANOMALIAS]
        
        hace_24h = datetime.now() - timedelta(hours=24)
        
        # Consumos de últimas 24h
        consumos = list(coll_consumos.find({
            'propietario_id': propietario_id,
            'timestamp': {'$gte': hace_24h.isoformat()}
        }))
        
        if not consumos:
            raise HTTPException(status_code=404, detail="No hay datos para este cliente")
        
        consumos_kwh = [c['consumo_kwh'] for c in consumos]
        
        # Anomalías
        anomalias = list(coll_anomalias.find({
            'propietario_id': propietario_id,
            'timestamp_deteccion': {'$gte': hace_24h.isoformat()}
        }))
        
        anomalias_criticas = [a for a in anomalias if a.get('severidad') == 'crítica']
        
        # Verificar si es cliente sospechoso
        es_sospechoso = any(c.get('es_sospechoso', False) for c in consumos)
        
        return EstadisticasCliente(
            propietario_id=propietario_id,
            consumo_promedio_24h=round(sum(consumos_kwh) / len(consumos_kwh), 3),
            consumo_minimo=round(min(consumos_kwh), 3),
            consumo_maximo=round(max(consumos_kwh), 3),
            consumo_noche_promedio=round(
                sum(c['consumo_kwh'] for c in consumos if c['hora'] in [0,1,2,3,4,5,23]) / 
                len([c for c in consumos if c['hora'] in [0,1,2,3,4,5,23]]) 
                if [c for c in consumos if c['hora'] in [0,1,2,3,4,5,23]] else 0, 3
            ),
            anomalias_detectadas=len(anomalias),
            anomalias_criticas=len(anomalias_criticas),
            es_cliente_sospechoso=es_sospechoso
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/estadisticas/resumen", response_model=ResumenAnomalia)
async def obtener_resumen_anomalias(horas: int = Query(24, ge=1, le=720)):
    """Obtiene resumen global de anomalías"""
    try:
        hace_x_horas = datetime.now() - timedelta(hours=horas)
        
        db = get_db()
        coll = db[COLLECTION_ANOMALIAS]
        
        anomalias = list(coll.find({
            'timestamp_deteccion': {'$gte': hace_x_horas.isoformat()}
        }))
        
        anomalias_criticas = [a for a in anomalias if a.get('severidad') == 'crítica']
        anomalias_altas = [a for a in anomalias if a.get('severidad') == 'alta']
        anomalias_medias = [a for a in anomalias if a.get('severidad') == 'media']
        
        clientes_afectados = len(set(a['propietario_id'] for a in anomalias))
        
        # Tipos más frecuentes
        tipos_contador = {}
        for a in anomalias:
            for tipo in a.get('tipos_anomalia', []):
                tipos_contador[tipo] = tipos_contador.get(tipo, 0) + 1
        
        tipos_mas_frecuentes = sorted(
            tipos_contador.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return ResumenAnomalia(
            total_anomalias=len(anomalias),
            anomalias_criticas=len(anomalias_criticas),
            anomalias_altas=len(anomalias_altas),
            anomalias_medias=len(anomalias_medias),
            clientes_afectados=clientes_afectados,
            tipos_mas_frecuentes=[t[0] for t in tipos_mas_frecuentes]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========== ENDPOINTS: DASHBOARD ==========
@app.get("/api/dashboard/top-anomalias")
async def dashboard_top_anomalias(limit: int = Query(10, le=100)):
    """Obtiene clientes con más anomalías para dashboard"""
    try:
        db = get_db()
        coll = db[COLLECTION_ANOMALIAS]
        
        pipeline = [
            {
                '$group': {
                    '_id': '$propietario_id',
                    'total_anomalias': {'$sum': 1},
                    'anomalias_criticas': {
                        '$sum': {'$cond': [{'$eq': ['$severidad', 'crítica']}, 1, 0]}
                    },
                    'ultima_anomalia': {'$max': '$timestamp_deteccion'}
                }
            },
            {'$sort': {'total_anomalias': -1}},
            {'$limit': limit}
        ]
        
        resultados = list(coll.aggregate(pipeline))
        return {"clientes": resultados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========== ENDPOINTS PARA DATOS MENSUALES ==========

@app.get("/api/consumos/mensuales/{propietario_id}")
async def obtener_consumos_mensuales(propietario_id: str, año: int = Query(2026)):
    """Obtiene consumos mensuales de un cliente para un año"""
    try:
        db = get_db()
        coll = db["consumos_mensuales"]
        
        consumos = list(coll.find({
            'propietario_id': propietario_id,
            'mes_str': {'$regex': f'^{año}'}
        }).sort('mes', 1))
        
        return consumos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/estadisticas/mensual/{propietario_id}")
async def obtener_estadistica_mensual(propietario_id: str, mes: str):
    """Obtiene estadísticas detalladas de un cliente para un mes específico (formato: YYYY-MM)"""
    try:
        db = get_db()
        coll = db["consumos_mensuales"]
        
        doc = coll.find_one({
            'propietario_id': propietario_id,
            'mes_str': mes
        })
        
        if not doc:
            raise HTTPException(status_code=404, detail=f"No hay datos para {propietario_id} en {mes}")
        
        return doc
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard/comparativa-mensual")
async def comparativa_mensual(mes: str):
    """Compara consumo mensual entre todos los clientes (formato mes: YYYY-MM)"""
    try:
        db = get_db()
        coll = db["consumos_mensuales"]
        
        consumos = list(coll.find({
            'mes_str': mes
        }).sort('consumo_total', -1))
        
        return {
            'mes': mes,
            'total_clientes': len(consumos),
            'consumo_total_mes': sum(c.get('consumo_total', 0) for c in consumos),
            'consumo_promedio': sum(c.get('consumo_total', 0) for c in consumos) / len(consumos) if consumos else 0,
            'clientes': consumos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=False)
