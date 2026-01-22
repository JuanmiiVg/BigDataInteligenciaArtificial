# 📚 Documentación Técnica Completa

## Tabla de Contenidos

1. [Arquitectura del Sistema](#arquitectura)
2. [Stack Tecnológico](#stack)
3. [Configuración](#configuración)
4. [Componentes Core](#componentes)
5. [Base de Datos](#base-de-datos)
6. [API REST](#api-rest)
7. [Comandos Útiles](#comandos)
8. [Troubleshooting](#troubleshooting)

---

## 🏗️ Arquitectura {#arquitectura}

### Descripción General

El sistema implementa una arquitectura de tres capas para optimizar almacenamiento y procesamiento:

```
┌─────────────────┐
│   Kafka Stream  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Consumer Kafka + Detector Anomalías│
└────────┬────────────┬────────────────┘
         │            │
         ▼            ▼
   ┌─────────┐  ┌──────────────┐
   │ MongoDB │  │  PostgreSQL  │
   │         │  │              │
   │ Mensuales│  │ Diarios      │
   │Anomalías │  │ (Histórico)  │
   └────┬────┘  └──────┬───────┘
        │               │
        └───────┬───────┘
                │
                ▼
         Backend API
                │
                ▼
        Frontend Streamlit
```

### Capas de Datos

#### Capa Caliente - PostgreSQL (Consumos Diarios)
- **Tabla**: `consumos_diarios`
- **Volumen**: ~50 clientes × 24 horas/día × 365 días = ~438,000 registros/año
- **Propósito**: Histórico completo para auditoría, análisis detallados
- **Retención**: Indefinida (bajo costo en SQL)
- **Campos clave**:
  - `propietario_id`: ID del cliente
  - `fecha`: Día del registro
  - `hora`: Hora (0-23)
  - `consumo_kwh`: Consumo en ese intervalo
  - `anomalia_detectada`: Booleano
  - `score_anomalia`: Puntuación (0-1)
  - `severidad`: crítica, alta, media, baja, normal
  - `es_sospechoso`: Si el cliente tiene comportamiento sospechoso

#### Capa Fría - MongoDB (Consumos Mensuales y Anomalías)
- **Colecciones**: 
  - `consumos_mensuales`: Agregaciones mensuales
  - `anomalias_detectadas`: Anomalías en tiempo real
- **Propósito**: Análisis rápido, dashboards, reporting
- **Retención**: Indefinida (bajo costo en NoSQL)

### Flujo de Datos

```
1. INGESTA EN TIEMPO REAL
   Kafka Topic "consumos-data"
       ↓
   Consumer Kafka
       ├→ Detecta anomalías
       ├→ Guarda en PostgreSQL (consumos_diarios)
       └→ Guarda en MongoDB (anomalias_detectadas)

2. AGREGACIÓN DIARIA/MENSUAL
   Script aggregator.py (ejecutar nightly)
       ↓
   Lee consumos_diarios de PostgreSQL
       ↓
   Agrega por mes:
       - SUM(consumo_kwh) → consumo_total
       - AVG(consumo_kwh) → consumo_promedio
       - COUNT(anomalias) → anomalias_detectadas
       ↓
   Escribe en MongoDB (consumos_mensuales)

3. CONSULTA EN BACKEND
   Frontend/API
       ├→ Datos mensuales → MongoDB
       ├→ Datos diarios/histórico → PostgreSQL
       └→ Anomalías → MongoDB
```

### Optimizaciones Logradas

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Documentos MongoDB/año | 438,000 | 600 | 99.86% ↓ |
| Consulta mensual | Aggregation (lento) | Query directo | 100x+ rápido |
| Espacio MongoDB | ~1GB/año | ~10MB/año | 99% ↓ |
| Costo operacional | 100% | 10-20% | 80-90% ↓ |

---

## 🗂️ Stack Tecnológico {#stack}

| Componente | Tecnología | Puerto | Propósito |
|-----------|-----------|--------|----------|
| **Data Generator** | FastAPI | 8000 | Genera datos sintéticos |
| **Kafka Broker** | Confluent Kafka | 9092 | Message queue |
| **Kafka UI** | Kafka UI | 8080 | Monitor Kafka |
| **PostgreSQL** | PostgreSQL 15 | 5432 | Consumos diarios |
| **MongoDB** | MongoDB 7 | 27017 | Datos mensuales + anomalías |
| **Backend API** | FastAPI | 8001 | REST API |
| **Frontend** | Streamlit | 8501 | Dashboard web |
| **Zookeeper** | Zookeeper | 2181 | Coordinación Kafka |

---

## ⚙️ Configuración {#configuración}

### Variables de Entorno (`.env`)

```bash
# PostgreSQL
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
POSTGRES_DB=consumo_db

# MongoDB
MONGO_HOST=mongodb
MONGO_PORT=27017
MONGO_USER=admin
MONGO_PASSWORD=password
MONGO_DB=consumo_db

# Kafka
KAFKA_BROKER=kafka:9092
KAFKA_TOPIC=consumos-data

# API
API_HOST=0.0.0.0
API_PORT=8001
```

### Docker Compose

El archivo `docker-compose.yml` define 8 servicios:

- `zookeeper`: Coordinación
- `kafka`: Message broker
- `kafka-ui`: Monitor
- `data-generator`: API generadora
- `postgres`: BD relacional
- `mongodb`: BD NoSQL
- `consumer`: Procesador de eventos
- `backend`: API REST
- `frontend`: Dashboard Streamlit

---

## 🔧 Componentes Core {#componentes}

### 1. Data Generator API (`data_generator/api.py`)

**Framework**: FastAPI | **Puerto**: 8000

Genera datos sintéticos de consumo eléctrico con patrones realistas.

**Endpoints principales**:
```
GET /generar/cliente/{propietario_id}    # 24h de un cliente
GET /generar/todos                        # 24h de todos los clientes
POST /generar/batch                       # Batch personalizado
GET /health                               # Health check
```

**Características**:
- Patrón normal: base_consumption + varianza
- Patrón sospechoso: simulación de plantación
- Tipos de anomalía: cannabis, fraude, picos

### 2. Kafka Producer (`kafka_producer/producer.py`)

**Broker**: Confluent Kafka | **Topic**: `consumos-data`

Envía datos al stream de Kafka para procesamiento en tiempo real.

**Modos**:
- `--mode once`: Envía un batch y termina
- `--mode continuous`: Ingesta continua cada N minutos

**Ejemplo**:
```bash
docker exec consumo-producer python producer.py --mode continuous --interval 1 --clients 50
```

### 3. Kafka Consumer (`kafka_consumer/consumer.py`)

**Group ID**: `consumo-processor-group`

Pipeline de procesamiento:
```
Kafka Consumer
    ↓
Detector de Anomalías
    ├→ Z-Score estadístico (desv > 3σ)
    ├→ Spike detection (incremento > 150%)
    ├→ Patrón nocturno anómalo
    └→ Consumo constante sospechoso
    ↓
MongoDB: consumos_horarios
    ↓
Si anomalía → MongoDB: anomalias_detectadas
```

### 4. Backend REST API (`backend/api.py`)

**Framework**: FastAPI | **Puerto**: 8001 | **BD**: MongoDB + PostgreSQL

**Categorías de endpoints**:

#### CONSUMOS
```
GET /api/consumos/últimas24h/{id}       # 100 últimos registros
GET /api/consumos/rango                  # Rango de fechas
GET /api/consumos/mensuales/{id}        # Consumo mensual de cliente
```

#### ANOMALÍAS
```
GET /api/anomalias/últimas              # Top 50 recientes
GET /api/anomalias/cliente/{id}         # Anomalías de un cliente
GET /api/anomalias/críticas             # Solo críticas
```

#### ESTADÍSTICAS
```
GET /api/estadisticas/cliente/{id}      # Stats completas de cliente
GET /api/estadisticas/resumen           # Resumen global
GET /api/estadisticas/mensuales/{id}    # Stats mensuales
```

#### DASHBOARD
```
GET /api/dashboard/top-anomalias        # Top 10 clientes
GET /api/dashboard/resumen              # KPIs generales
```

### 5. Frontend Streamlit (`frontend/app.py`)

**Puerto**: 8501 | **Framework**: Streamlit con Plotly

**Páginas**:
1. **Dashboard Principal**: Resumen global, top 10 anomalías, KPIs
2. **Buscar Cliente**: Detalles individuales, histórico, gráficos
3. **Consumo Mensual**: Análisis por mes, comparativas
4. **Anomalías**: Tabla filtrable, distribuciones, estadísticas
5. **Análisis Avanzado**: Gráficos personalizados, heatmaps

---

## 🗄️ Base de Datos {#base-de-datos}

### PostgreSQL - Esquema

#### Tabla: `consumos_diarios`
```sql
CREATE TABLE consumos_diarios (
    id SERIAL PRIMARY KEY,
    propietario_id VARCHAR(20),
    fecha DATE,
    hora INT (0-23),
    consumo_kwh DECIMAL(10,2),
    anomalia_detectada BOOLEAN,
    score_anomalia DECIMAL(3,2),
    severidad VARCHAR(20),
    es_sospechoso BOOLEAN,
    timestamp_procesado TIMESTAMP
);

-- Índices
CREATE INDEX idx_propietario ON consumos_diarios(propietario_id);
CREATE INDEX idx_fecha ON consumos_diarios(fecha);
CREATE INDEX idx_propietario_fecha ON consumos_diarios(propietario_id, fecha);
```

#### Tabla: `consumos_diarios_archivo`
```sql
-- Estructura idéntica a consumos_diarios
-- Almacena datos > 30 días (configurable)
```

#### Tabla: `log_archivado`
```sql
CREATE TABLE log_archivado (
    id SERIAL PRIMARY KEY,
    fecha_archivado TIMESTAMP,
    registros_movidos INT,
    espacio_liberado_mb DECIMAL(10,2),
    estado VARCHAR(20)
);
```

### MongoDB - Esquema

#### Colección: `consumos_mensuales`
```javascript
{
    _id: "CLI_00001_2026-01",
    propietario_id: "CLI_00001",
    mes: ISODate("2026-01-01"),
    mes_str: "2026-01",
    consumo_total: 720.5,
    consumo_promedio: 23.8,
    consumo_minimo: 10.2,
    consumo_maximo: 45.3,
    anomalias_detectadas: 3,
    anomalias_criticas: 1,
    consumo_noche_promedio: 15.2,
    consumo_punta_promedio: 35.8
}

// Índice
db.consumos_mensuales.createIndex({ "mes_str": 1 })
db.consumos_mensuales.createIndex({ "propietario_id": 1 })
```

#### Colección: `anomalias_detectadas`
```javascript
{
    _id: ObjectId,
    propietario_id: "CLI_00045",
    timestamp_consumo: ISODate(),
    timestamp_deteccion: ISODate(),
    consumo_kwh: 8.5,
    hora: 2,
    tipos_anomalia: [
        "consumo_noche_anomalo",
        "plantacion_cannabis"
    ],
    score_anomalia: 0.95,
    severidad: "crítica",
    es_sospechoso: true
}

// Índices
db.anomalias_detectadas.createIndex({ "propietario_id": 1 })
db.anomalias_detectadas.createIndex({ "timestamp_deteccion": -1 })
```

---

## 📡 API REST {#api-rest}

### Ejemplos con curl

#### Obtener últimas 24h de un cliente
```bash
curl "http://localhost:8001/api/consumos/últimas24h/CLI_00001"
```

#### Obtener anomalías críticas
```bash
curl "http://localhost:8001/api/anomalias/críticas"
```

#### Obtener consumo mensual
```bash
curl "http://localhost:8001/api/consumos/mensuales/CLI_00001"
```

#### Obtener estadísticas de cliente
```bash
curl "http://localhost:8001/api/estadisticas/cliente/CLI_00001"
```

#### Dashboard - Top anomalías
```bash
curl "http://localhost:8001/api/dashboard/top-anomalias"
```

### Documentación Interactiva
```
http://localhost:8001/docs
```

---

## ⚡ Comandos Útiles {#comandos}

### Iniciar/Parar Sistema

```bash
# Construir y lanzar todo
docker-compose up -d --build

# Verificar que todo está corriendo
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Parar todo
docker-compose down

# Parar y limpiar volúmenes
docker-compose down -v
```

### Generar Datos

```bash
# Una tanda (50 clientes)
docker exec consumo-producer python producer.py --mode once --clients 50

# Continuo (cada minuto)
docker exec consumo-producer python producer.py --mode continuous --interval 1 --clients 50

# Personalizado (100 clientes, cada 2 minutos)
docker exec consumo-producer python producer.py --mode continuous --interval 2 --clients 100
```

### Datos Mensuales (Agregación)

```bash
# Generar consumos mensuales desde diarios
docker exec consumo-consumer python aggregator.py

# Generar mes específico
docker exec consumo-consumer python aggregator.py 2026-01

# Ver consumos mensuales
docker exec consumo-mongodb mongosh -u admin -p password --eval "
  db.getSiblingDB('consumo_db').consumos_mensuales.find({}).pretty()
"
```

### Gestión de Datos (Archivado)

```bash
# Archivar normal (30 días default)
docker exec consumo-consumer python archivador.py

# Archivar agresivo (7 días)
docker exec consumo-consumer python archivador.py --agresivo

# Ver reporte SIN hacer cambios
docker exec consumo-consumer python archivador.py --reporte

# Solo PostgreSQL
docker exec consumo-consumer python archivador.py --solo-postgres

# Solo MongoDB
docker exec consumo-consumer python archivador.py --solo-mongodb
```

### Restaurar Datos

```bash
# Listar datos archivados
docker exec consumo-consumer python restaurador.py --listar

# Restaurar rango específico
docker exec consumo-consumer python restaurador.py \
  --restaurar \
  --fecha-inicio 2025-12-01 \
  --fecha-fin 2025-12-31

# Eliminar permanentemente (datos > 365 días)
docker exec consumo-consumer python restaurador.py \
  --eliminar-permanentemente \
  --dias 365
```

### Consultar Bases de Datos

#### PostgreSQL

```bash
# Conectar
docker exec -it consumo-postgres psql -U postgres -d consumo_db

# Dentro de psql:
\dt                                    # Ver todas las tablas
SELECT COUNT(*) FROM consumos_diarios; # Contar registros diarios
SELECT COUNT(*) FROM consumos_diarios_archivo; # Contar archivados
SELECT * FROM consumos_diarios LIMIT 5; # Ver primeros 5 registros
SELECT * FROM log_archivado ORDER BY fecha_archivado DESC LIMIT 10; # Ver logs
```

#### MongoDB

```bash
# Conectar
docker exec -it consumo-mongodb mongosh -u admin -p password

# Dentro de mongosh:
use consumo_db
db.consumos_mensuales.count()        # Contar mensuales
db.anomalias_detectadas.find().limit(5)  # Ver anomalías
db.consumos_mensuales.find({propietario_id: "CLI_00001"})  # Buscar cliente
db.log_archivado_mongo.find().sort({_id: -1}).limit(10)   # Ver logs
```

### Verificar Datos

```bash
# PostgreSQL - Consumos Diarios
docker exec consumo-postgres psql -U postgres -d consumo_db -c "SELECT COUNT(*) FROM consumos_diarios;"

# MongoDB - Datos Mensuales
docker exec consumo-mongodb mongosh -u admin -p password --eval "db.consumos_mensuales.find().count()"
```

### Acceso Rápido

```
Frontend:        http://localhost:8501
API REST:        http://localhost:8001
API Docs:        http://localhost:8001/docs
Kafka UI:        http://localhost:8080
MongoDB CLI:     mongosh "mongodb://admin:password@localhost:27017"
PostgreSQL CLI:  psql -h localhost -U postgres -d consumo_db
```

---

## 🔍 Troubleshooting {#troubleshooting}

### Problema: Los servicios no inician

**Solución**:
```bash
# Limpiar todo y reiniciar
docker-compose down -v
docker-compose up -d --build

# Ver logs
docker-compose logs -f
```

### Problema: PostgreSQL no conecta

**Solución**:
```bash
# Verificar que el contenedor está corriendo
docker ps | grep postgres

# Verificar logs
docker logs consumo-postgres

# Conectar manualmente
docker exec -it consumo-postgres psql -U postgres -d consumo_db
```

### Problema: MongoDB no tiene datos

**Solución**:
```bash
# Generar datos
docker exec consumo-producer python producer.py --mode once --clients 50

# Verificar Consumer está corriendo
docker ps | grep consumer

# Ver logs del Consumer
docker logs consumo-consumer
```

### Problema: Frontend da error de conexión

**Solución**:
```bash
# Verificar que Backend está corriendo en puerto 8001
docker exec consumo-backend lsof -i :8001

# Reiniciar Backend
docker restart consumo-backend
```

### Problema: Datos mensuales no se generan

**Solución**:
```bash
# Ejecutar agregador manualmente
docker exec consumo-consumer python aggregator.py

# Ver logs
docker logs consumo-consumer

# Verificar datos en PostgreSQL
docker exec consumo-postgres psql -U postgres -d consumo_db -c "SELECT COUNT(*) FROM consumos_diarios;"
```

### Limpiar espacios en disco

```bash
# Eliminar contenedores parados
docker container prune -f

# Eliminar imágenes sin usar
docker image prune -f

# Eliminar volúmenes sin usar
docker volume prune -f

# Eliminar todo
docker system prune -f
```

---

## 📚 Referencias Adicionales

- **README.md**: Guía general y características
- **QUICK_START.md**: Inicio en 60 segundos
- API Docs: http://localhost:8001/docs
- Kafka UI: http://localhost:8080
