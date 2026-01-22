"""
API de generación de datos de consumo
Simula consumos de 24 horas con patrones realistas y anomalías
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    BASE_CONSUMPTION, PEAK_CONSUMPTION, NIGHT_CONSUMPTION,
    CONSUMPTION_VARIANCE, NUM_CLIENTES, SUSPICIOUS_PERCENT,
    NIGHT_HOURS, PEAK_HOURS, API_HOST, API_PORT
)

app = FastAPI(title="Consumo Data Generator API")

# ========== MODELOS ==========
class ConsumoHorario(BaseModel):
    propietario_id: str
    timestamp: str
    consumo_kwh: float
    hora: int
    anomalia_esperada: bool
    tipo_anomalia: str | None = None

class ReporteConsumo(BaseModel):
    propietario_id: str
    consumo_total_24h: float
    consumo_promedio_horario: float
    consumo_noche: float
    consumo_punta: float
    pct_noche: float
    anomalia_detectada: bool
    tipo_anomalia: str | None = None

# ========== GENERADOR DE CONSUMOS ==========
class ConsumptionGenerator:
    def __init__(self, propietario_id: str, es_sospechoso: bool = False):
        self.propietario_id = propietario_id
        self.es_sospechoso = es_sospechoso
        np.random.seed(hash(propietario_id) % 2**32)
        
    def generar_consumo_24h(self, date: datetime = None) -> tuple[List[ConsumoHorario], ReporteConsumo]:
        """Genera consumo para 24 horas"""
        if date is None:
            date = datetime.now() - timedelta(days=1)
        
        consumos = []
        consumo_total = 0
        consumo_noche = 0
        consumo_punta = 0
        count_noche = 0
        count_punta = 0
        
        for hora in range(24):
            timestamp = date + timedelta(hours=hora)
            
            # Consumo base según hora del día
            if hora in NIGHT_HOURS:
                consumo_base = NIGHT_CONSUMPTION
                es_noche = True
            elif hora in PEAK_HOURS:
                consumo_base = PEAK_CONSUMPTION
                es_punta = True
            else:
                consumo_base = BASE_CONSUMPTION
                es_punta = False
            
            # Varianza normal
            varianza = np.random.normal(1.0, CONSUMPTION_VARIANCE)
            consumo = consumo_base * max(0.1, varianza)
            
            # Comportamiento sospechoso
            tipo_anomalia = None
            anomalia_esperada = False
            
            if self.es_sospechoso:
                rand = np.random.random()
                
                # 30% de probabilidad: plantación de marihuana (consumo muy alto en noche)
                if hora in NIGHT_HOURS and rand < 0.30:
                    consumo = consumo * np.random.uniform(5, 15)  # 5-15x normal
                    tipo_anomalia = "plantacion_cannabis"
                    anomalia_esperada = True
                
                # 20% de probabilidad: pico repentino (crecimiento anómalo)
                elif rand < 0.50:
                    consumo = consumo * np.random.uniform(3, 8)  # 3-8x normal
                    tipo_anomalia = "pico_anomalo"
                    anomalia_esperada = True
                
                # 15% de probabilidad: consumo constante anómalo (fraude)
                elif rand < 0.65:
                    consumo = PEAK_CONSUMPTION * 0.8
                    tipo_anomalia = "consumo_constante_anomalo"
                    anomalia_esperada = True
            
            consumo_total += consumo
            
            if hora in NIGHT_HOURS:
                consumo_noche += consumo
                count_noche += 1
            if hora in PEAK_HOURS:
                consumo_punta += consumo
                count_punta += 1
            
            consumos.append(ConsumoHorario(
                propietario_id=self.propietario_id,
                timestamp=timestamp.isoformat(),
                consumo_kwh=round(consumo, 3),
                hora=hora,
                anomalia_esperada=anomalia_esperada,
                tipo_anomalia=tipo_anomalia
            ))
        
        pct_noche = (consumo_noche / consumo_total * 100) if consumo_total > 0 else 0
        
        reporte = ReporteConsumo(
            propietario_id=self.propietario_id,
            consumo_total_24h=round(consumo_total, 3),
            consumo_promedio_horario=round(consumo_total / 24, 3),
            consumo_noche=round(consumo_noche, 3),
            consumo_punta=round(consumo_punta, 3),
            pct_noche=round(pct_noche, 2),
            anomalia_detectada=any(c.anomalia_esperada for c in consumos),
            tipo_anomalia=next((c.tipo_anomalia for c in consumos if c.anomalia_esperada), None)
        )
        
        return consumos, reporte

# ========== ENDPOINTS ==========
@app.get("/health")
async def health_check():
    """Verificar que la API está funcionando"""
    return {"status": "ok", "service": "data_generator"}

@app.get("/generar/cliente/{propietario_id}")
async def generar_consumo_cliente(propietario_id: str, es_sospechoso: bool = False):
    """Genera 24 horas de consumo para un cliente"""
    try:
        gen = ConsumptionGenerator(propietario_id, es_sospechoso)
        consumos, reporte = gen.generar_consumo_24h()
        return {
            "consumos_horarios": consumos,
            "reporte_diario": reporte
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generar/todos")
async def generar_consumo_todos(fecha: str = None):
    """Genera consumo para todos los clientes (50 normales + 5 sospechosos)"""
    try:
        if fecha:
            try:
                date = datetime.fromisoformat(fecha)
            except:
                raise HTTPException(status_code=400, detail="Fecha inválida. Use formato ISO: YYYY-MM-DD")
        else:
            date = datetime.now() - timedelta(days=1)
        
        resultados = []
        num_sospechosos = max(1, int(NUM_CLIENTES * SUSPICIOUS_PERCENT / 100))
        
        for i in range(NUM_CLIENTES):
            cliente_id = f"CLI_{i+1:05d}"
            es_sospechoso = i >= (NUM_CLIENTES - num_sospechosos)
            
            gen = ConsumptionGenerator(cliente_id, es_sospechoso)
            consumos, reporte = gen.generar_consumo_24h(date)
            
            resultados.append({
                "cliente_id": cliente_id,
                "es_sospechoso": es_sospechoso,
                "consumos": consumos,
                "reporte": reporte
            })
        
        return {
            "fecha": date.isoformat(),
            "total_clientes": NUM_CLIENTES,
            "clientes_sospechosos": num_sospechosos,
            "resultados": resultados
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generar/batch")
async def generar_batch_personalizado(
    num_clientes: int = 10,
    num_sospechosos: int = 2,
    fecha: str = None
):
    """Genera un batch personalizado de datos"""
    try:
        if num_sospechosos > num_clientes:
            raise HTTPException(status_code=400, detail="Sospechosos no puede ser > clientes")
        
        if fecha:
            try:
                date = datetime.fromisoformat(fecha)
            except:
                raise HTTPException(status_code=400, detail="Fecha inválida")
        else:
            date = datetime.now() - timedelta(days=1)
        
        resultados = []
        
        for i in range(num_clientes):
            cliente_id = f"CLI_{i+1:05d}"
            es_sospechoso = i >= (num_clientes - num_sospechosos)
            
            gen = ConsumptionGenerator(cliente_id, es_sospechoso)
            consumos, reporte = gen.generar_consumo_24h(date)
            
            resultados.append({
                "cliente_id": cliente_id,
                "es_sospechoso": es_sospechoso,
                "consumos": consumos,
                "reporte": reporte
            })
        
        return {
            "fecha": date.isoformat(),
            "total_clientes": num_clientes,
            "clientes_sospechosos": num_sospechosos,
            "resultados": resultados
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=False)
