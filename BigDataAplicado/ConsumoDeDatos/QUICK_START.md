# 🚀 Guía Rápida de Inicio

## 60 segundos para tener el sistema funcionando

### Opción 1: Windows

```cmd
REM Abrir terminal en ConsumoDeDatos
cd ConsumoDeDatos

REM Ejecutar
start.bat

REM Esperar 2-3 minutos a que se inicien todos los servicios
REM Luego abrir en navegador: http://localhost:8501
```

### Opción 2: Linux/Mac

```bash
cd ConsumoDeDatos
chmod +x start.sh
./start.sh

# En otra terminal
chmod +x scripts/*.sh
./scripts/watch_logs.sh
```

### Opción 3: Terminal Manual

```bash
cd ConsumoDeDatos
docker-compose up --build
```

---

## ✅ ¿Cómo sé que funciona?

### 1. Verificar servicios activos

```bash
docker-compose ps
```

Deberías ver 7 contenedores en estado `healthy`:
- mongodb
- zookeeper
- kafka
- data-generator
- kafka-producer
- kafka-consumer
- backend
- frontend

### 2. Abrir dashboard

Ve a: **http://localhost:8501**

Deberías ver el dashboard con métricas y gráficos

### 3. Verificar datos en MongoDB

```bash
docker exec -it consumo_mongodb mongosh
> use consumo_db
> db.anomalias_detectadas.count()
```

---

## 🎮 Próximos Pasos

### Generar más datos

```bash
# Una sola vez
docker exec consumo_producer python kafka_producer/producer.py --mode once --clients 100

# Continuamente (cada minuto)
docker exec consumo_producer python kafka_producer/producer.py --mode continuous --interval 1
```

### Ver anomalías críticas

```bash
curl http://localhost:8001/api/anomalias/críticas | jq .
```

### Ver estadísticas de un cliente

```bash
curl http://localhost:8001/api/estadisticas/cliente/CLI_00045 | jq .
```

---

## 🐛 Problemas Comunes

| Problema | Solución |
|----------|----------|
| "Error: Connection refused" | Esperar 30-60 seg a que se inicie |
| "Streamlit no carga" | Verificar: `curl http://localhost:8001/health` |
| "No hay datos" | Ejecutar: `docker-compose logs -f kafka-producer` |
| "Puerto ya en uso" | `docker-compose down` y reintentar |

---

## 🔗 URLs Útiles

| Servicio | URL |
|----------|-----|
| Dashboard | http://localhost:8501 |
| API Backend | http://localhost:8001 |
| API Generadora | http://localhost:8000 |
| Documentación API | http://localhost:8001/docs |
| MongoDB Express | (opcional) |

---

## 📊 Ejemplo: Flujo de Datos

```
API Generadora (8000)
    ↓
Kafka Producer
    ↓
Kafka Broker (9092)
    ↓
Kafka Consumer (detecta anomalías)
    ↓
MongoDB (almacena)
    ↓
Backend API (8001) ← Frontend (8501)
```

---

## 🎯 Que ver en el Dashboard

1. **Dashboard Principal**: Resumen de anomalías últimas 24h
2. **Buscar Cliente**: Detalles individuales (ej: CLI_00001)
3. **Anomalías**: Lista completa con filtros
4. **Análisis**: Gráficos avanzados

---

## 💡 Tips

- El sistema genera datos sintéticos realistas
- ~10% de clientes son sospechosos (posible plantación)
- Las anomalías se detectan en tiempo real (< 1 segundo)
- Puedes consultar la API sin usar el dashboard

---

¿Listo? ¡Abre http://localhost:8501 y empieza a explorar! 🎉
