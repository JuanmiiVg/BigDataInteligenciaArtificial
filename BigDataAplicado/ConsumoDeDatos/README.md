# 🔌 Sistema de Monitoreo de Consumo en Tiempo Real - v2.0

Sistema **Enterprise-Ready** de detección de anomalías en consumo de energía eléctrica con **Kafka**, **PostgreSQL**, **MongoDB**, análisis en tiempo real y **gestión inteligente de Big Data**.

## ⚡ Características Principales

- 🚨 **Detección de anomalías en tiempo real** (plantaciones, fraude, picos)
- 📊 **Almacenamiento inteligente** con PostgreSQL + MongoDB
- 📅 **Análisis mensuales automáticos** con agregación diaria
- 💾 **Gestión inteligente de datos** (archivado, restauración)
- 🌐 **Dashboard Streamlit** con 5 páginas interactivas
- 🔌 **API REST** con 15+ endpoints (FastAPI)
- 🐳 **Docker Compose** con 8 servicios pre-configurados
- ⚡ **Escalable** para 50 a 10,000+ clientes

## 🚀 Inicio Rápido (60 segundos)

### Windows
```bash
cd ConsumoDeDatos
docker-compose up -d --build

# Esperar 30-60 segundos a que levante todo
# Luego abre en navegador: http://localhost:8501
```

### Linux/Mac
```bash
cd ConsumoDeDatos
chmod +x start.sh
./start.sh
```

## 🌐 Acceso Inmediato

```
🌐 Frontend:            http://localhost:8501
🔌 API REST:            http://localhost:8001
📚 Documentación API:    http://localhost:8001/docs
```

## 📚 Documentación

| Documento | Contenido |
|-----------|----------|
| **[QUICK_START.md](QUICK_START.md)** | ⚡ Guía de inicio rápido (60 segundos) |
| **[DOCS.md](DOCS.md)** | 📖 Documentación técnica completa |

### En DOCS.md encontrarás:
- Arquitectura completa del sistema
- Configuración y variables de entorno
- Descripción de todos los componentes
- Esquema de bases de datos (PostgreSQL + MongoDB)
- Todos los endpoints API
- Comandos útiles y troubleshooting
- Ejemplos de uso

## 🗂️ Stack Tecnológico

| Componente | Propósito | Puerto |
|-----------|----------|--------|
| **Kafka + Zookeeper** | Streaming datos en tiempo real | 9092, 2181 |
| **PostgreSQL 15** | Consumos diarios (histórico) | 5432 |
| **MongoDB 7** | Consumos mensuales + Anomalías | 27017 |
| **FastAPI** | REST API Backend | 8001 |
| **Streamlit** | Dashboard web | 8501 |
| **Python 3.9+** | Lógica de negocio | - |
| **Docker** | Containerización | - |

## 🎯 Casos de Uso Principales

### 1. Detectar Anomalías en Tiempo Real
- 🚨 **Plantaciones** de cannabis (consumo alto nocturno)
- 💡 **Fraude** eléctrico (consumo constante anómalo)
- 📈 **Picos** anómalos (incrementos > 150%)
- 🌙 **Patrones** sospechosos

### 2. Analizar Consumo Mensual
- Agregación automática de datos diarios
- Comparativas por franja horaria
- Score de anomalía mensual
- **10-50x más rápido** que datos diarios

### 3. Gestionar Ciclo de Vida de Datos
- ✅ Archivado automático (datos > 30 días)
- ✅ Restauración bajo demanda
- ✅ Auditoría completa de operaciones
- ✅ Reducción 80-90% en espacio

## 📊 Mejoras v2.0

| Aspecto | Antes (v1.0) | Después (v2.0) |
|---------|-------------|----------------|
| Almacenamiento | Solo MongoDB | PostgreSQL + MongoDB |
| Datos Mensuales | Manual | Automático |
| Tamaño activo | Crece infinito | Fijo 30 días |
| Velocidad queries | 🐌 Lenta | ⚡ 100x más rápida |
| Consultas mensuales | NO | SÍ (web + API) |
| Escalabilidad | Limitada | Hasta 10,000+ clientes |

## 🔧 Comandos Esenciales

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Parar sistema
docker-compose down

# Limpiar todo (incluyendo volúmenes)
docker-compose down -v

# Generar datos de prueba
docker exec consumo-producer python producer.py --mode once --clients 50

# Ver estado de servicios
docker-compose ps

# Archivar datos > 30 días
docker exec consumo-consumer python archivador.py

# Listar datos archivados
docker exec consumo-consumer python restaurador.py --listar
```

## 📖 ¿Dónde Buscar?

- **¿Cómo empezar?** → [QUICK_START.md](QUICK_START.md)
- **¿Cómo funciona?** → [DOCS.md](DOCS.md) (Sección: Arquitectura)
- **¿Qué bases de datos?** → [DOCS.md](DOCS.md) (Sección: Base de Datos)
- **¿Qué endpoints API?** → [DOCS.md](DOCS.md) (Sección: API REST)
- **¿Qué comandos?** → [DOCS.md](DOCS.md) (Sección: Comandos Útiles)
- **¿Error?** → [DOCS.md](DOCS.md) (Sección: Troubleshooting)

## 🚨 Requisitos Previos

- Docker y Docker Compose
- 4GB RAM disponible (mínimo)
- Puertos libres: 8000, 8001, 8501, 9092, 5432, 27017

## 💡 Tips

1. **Primera vez**: Ejecuta `docker-compose up -d --build` y espera 60 segundos
2. **Ver datos**: Abre http://localhost:8501 en navegador
3. **Generar datos**: Usa el botón en el dashboard o comando Docker
4. **Problemas**: Consulta [DOCS.md](DOCS.md) sección Troubleshooting
5. **APIs**: Documentación interactiva en http://localhost:8001/docs

---

**Para documentación técnica detallada, ver [DOCS.md](DOCS.md)**
