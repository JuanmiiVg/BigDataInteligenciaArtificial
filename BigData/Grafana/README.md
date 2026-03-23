# Laboratorio Grafana - Visualización de Métricas

## 🚀 Inicio Rápido

1. **Ejecuta el laboratorio:**
   ```bash
   start_lab.bat
   ```

2. **Accede a los servicios:**
   - **Grafana**: http://localhost:3000 (admin/admin123)
   - **Prometheus**: http://localhost:9090
   - **Métricas**: http://localhost:8000/metrics

3. **Para detener:**
   ```bash
   stop_lab.bat
   ```

## 📊 Métricas Disponibles

El simulador genera estas métricas para el laboratorio:

- `fake_cpu_usage`: Uso de CPU simulado (0-100%)
- `fake_requests_total`: Contador de peticiones HTTP
- `fake_memory_usage_bytes`: Uso de memoria en bytes

## 🔧 Configuración de Grafana

### Paso 1: Configurar Data Source
1. Ve a Configuration > Data Sources
2. Add data source > Prometheus
3. URL: `http://prometheus:9090`
4. Save & Test

### Paso 2: Crear Paneles Obligatorios

**Panel 1 - CPU:**
- Métrica: `fake_cpu_usage`
- Visualización: Time series

**Panel 2 - Peticiones:**
- Métrica: `fake_requests_total`
- Visualización: Time series o Stat

## 📁 Estructura del Proyecto

```
Grafana/
├── docker-compose.yml      # Orquestación de contenedores
├── prometheus.yml          # Configuración de Prometheus
├── start_lab.bat          # Script de inicio
├── stop_lab.bat           # Script de parada
├── simulator/
│   └── metrics_simulator.py  # Generador de métricas
└── README.md              # Esta documentación
```

## 🔍 Verificación

- **Prometheus funcionando**: http://localhost:9090/targets
- **Métricas disponibles**: http://localhost:8000/metrics
- **Grafana funcionando**: http://localhost:3000

## ⚠️ Solución de Problemas

**Si los contenedores no inician:**
```bash
docker-compose logs
```

**Si Prometheus no encuentra el simulador:**
- Verifica que all targets estén "UP" en http://localhost:9090/targets

**Si Grafana no conecta con Prometheus:**
- Usa la URL interna: http://prometheus:9090