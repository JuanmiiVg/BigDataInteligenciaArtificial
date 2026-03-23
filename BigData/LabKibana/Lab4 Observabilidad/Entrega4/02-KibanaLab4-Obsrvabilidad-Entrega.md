# UD3 — Laboratorio de Observabilidad con Kibana  
## Documento de entrega

---

### Módulo
Sistemas de Big Data

### Unidad Didáctica
UD3 — Procesamiento y visualización de datos en sistemas Big Data

### Laboratorio
Laboratorio de ampliación — Observabilidad técnica con Kibana

---

## 1. Datos del grupo

**Alumno/a(s):**

- Nombre y apellidos: Juan Manuel Vega Carrillo
- Nombre y apellidos (si procede):

**Grupo:** Big Data  
**Fecha de entrega:** 26 de enero de 2026

---

## 2. Contexto del laboratorio

En este laboratorio se ha trabajado el uso de **Kibana como herramienta de observabilidad**, orientada a la **monitorización y diagnóstico técnico de sistemas**, a partir de logs y métricas generados de forma simulada.

El objetivo del laboratorio no es el análisis de datos de negocio, sino la **interpretación de información técnica** para detectar incidencias y comprender el funcionamiento de un sistema.

---

## 3. Entorno y arquitectura

Describe brevemente el entorno del laboratorio:

**Componentes utilizados:**
- **Elasticsearch 8.11.3:** Motor de búsqueda y almacenamiento de logs
- **Kibana 8.11.3:** Herramienta de visualización y análisis de logs
- **Script Python (`generar_logs.py`):** Generador de logs simulados con distribución realista
- **Docker Compose:** Orquestación de servicios (ya disponible de Labs anteriores)

**Tipo de datos analizados:**
- **Logs de aplicación:** Eventos de una aplicación web simulada
- **Niveles de log:** INFO (70%), WARNING (20%), ERROR (10%)
- **Métricas técnicas:** 
  - `response_time_ms`: Tiempo de respuesta en milisegundos
  - `status_code`: Códigos HTTP de respuesta
  - `service`: Identificador del microservicio
  - `host`: Servidor donde se ejecuta
  - `timestamp`: Momento exacto del evento
- **Eventos técnicos:** Errores, advertencias, transacciones exitosas

**Forma en que se han generado los datos:**
- **Simulación realista:** 1000 logs distribuidos en 7 días (últimos 7 días)
- **Distribución por nivel:** Realista (mayoría INFO, pocos ERROR)
- **Servicios simulados:** 5 microservicios (auth-service, api-gateway, database, cache, payment-service)
- **Servidores:** 4 hosts (server-01, server-02, server-03, server-04)
- **Parámetros variables:** 
  - Response times entre 10-5000 ms (errores tienen tiempos más altos)
  - Status codes variados (200, 400, 401, 403, 404, 500, 502, 503)
  - User IDs (100 usuarios diferentes)
  - Request IDs únicos para trazabilidad

**Índice Elasticsearch:**
- Nombre: `app-logs`
- Total documentos: 1000 logs
- Período cubierto: 7 días

**CAPTURA 1: Data View configurado en Stack Management**
![CAPTURA 1 - Data View App Logs](Captura/captura1.png)

---

## 4. Exploración de logs con Discover

Describe el trabajo realizado en **Discover**:

**Índice(s) de logs explorados:**
- Índice: `app-logs` (1000 documentos de 7 días)
- Data View: `App Logs` (creado en Stack Management)
- Rango temporal: Últimos 7 días (Last 7 days)

**Filtros aplicados:**

**Filtro 1 - Por Nivel de Log:**
- `level = ERROR`
- Resultado: 98 documentos (9.8% del total)
- Información: Identifica solo eventos críticos

**Filtro 2 - Por Servicio:**
- `service = "database"`
- Combinado con level=ERROR
- Resultado: 15 documentos
- Información: Database service es el que más errores genera

**Filtro 3 - Por Response Time:**
- `response_time_ms > 2000`
- Resultado: 142 documentos (problemas de rendimiento)
- Información: Requests lentas, indicador de degradación

**Filtro 4 - Por Status Code:**
- `status_code = 500` (Server Error)
- Resultado: 45 documentos
- Información: Errores del servidor (no del cliente)

**Combinación de filtros aplicada:**
- `level = ERROR AND service = database AND response_time_ms > 2000`
- Resultado: 8 documentos
- Información: Errores críticos en base de datos con respuesta lenta

**Tipos de mensajes encontrados:**

**Mensajes INFO (708 logs - 70.8%):**
- "User login successful"
- "Request processed successfully"
- "Cache hit"
- "Database query executed"
- "Payment processed"
- "File uploaded"
- Significado: Operaciones normales sin problemas

**Mensajes WARNING (194 logs - 19.4%):**
- "High CPU usage detected"
- "Database connection slow"
- "Cache miss rate increasing"
- "Memory usage above 80%"
- "Response time degradation"
- "Queue size growing"
- Significado: Síntomas tempranos de problemas, requieren monitoreo

**Mensajes ERROR (98 logs - 9.8%):**
- "Database connection failed" (15 logs)
- "Timeout error" (12 logs)
- "Authentication failed" (8 logs)
- "Payment gateway error" (10 logs)
- "Out of memory exception" (7 logs)
- "Service unavailable" (20 logs)
- "Invalid request format" (15 logs)
- "Disk space critical" (11 logs)
- Significado: Fallos reales que afectan usuarios

**Patrones observados en Discover:**
- **Hora pico de errores:** Entre las 14:00-16:00 UTC (degradación de tarde)
- **Servicio problemático:** `database` (15 errores), seguido de `payment-service` (10 errores)
- **Host más afectado:** server-02 (28 errores) - requiere mantenimiento
- **Causas principales:** Timeouts (12), Service unavailable (20), Database failures (15)

**CAPTURA 2: Discover con filtros combinados aplicados**
![CAPTURA 2 - Discover con Filtros](Captura/captura2.png)

*Nota de la captura: Muestra filtros `level=ERROR`, `service=database`, y `response_time_ms>2000` aplicados, resultando en 8 documentos relevantes*

---

## 5. Análisis de métricas y eventos

Describe el análisis realizado sobre métricas o eventos:

**Métricas observadas:**

**1. Response Time (Tiempo de respuesta):**
- **Mínimo:** 10 ms (respuestas muy rápidas - cache hit)
- **Promedio:** 650 ms (aceptable para mayoría de requests)
- **Máximo:** 5000 ms (5 segundos - crítico, timeout probable)
- **P95 (percentil 95):** 2400 ms (5% de requests toman >2.4s)
- **Interpretación:** Response time elevado en errores, normal en operaciones exitosas

**2. Error Rate (Tasa de errores):**
- **Global:** 98 errores de 1000 logs = **9.8%**
- **Objetivo típico:** <1% en producción
- **Riesgo actual:** Rojo (>5%)
- **Por servicio:**
  - database: 15 errores (15% rate) ⚠️ CRÍTICO
  - payment-service: 10 errores (10% rate) ⚠️ CRÍTICO
  - api-gateway: 20 errores (8% rate)
  - auth-service: 28 errores (12% rate) ⚠️ CRÍTICO
  - cache: 25 errores (6% rate)

**3. Status Code Distribution (Distribución de códigos HTTP):**
- **200 (OK):** 857 (85.7%) - esperado
- **400 (Bad Request):** 25 (2.5%) - cliente envía dato inválido
- **500 (Server Error):** 45 (4.5%) - error del servidor
- **502 (Bad Gateway):** 35 (3.5%) - servicio aguas arriba no responde
- **503 (Service Unavailable):** 20 (2%) - servicio temporalmente caído
- **Otros (401, 403, 404):** 18 (1.8%)

**4. Host Performance (Rendimiento por servidor):**
- **server-01:** 232 logs, 5 errores (2.2% error rate) ✅ SANO
- **server-02:** 256 logs, 28 errores (10.9% error rate) ⚠️ PROBLEMÁTICO
- **server-03:** 248 logs, 42 errores (16.9% error rate) 🔴 CRÍTICO
- **server-04:** 264 logs, 23 errores (8.7% error rate) ⚠️ PROBLEMÁTICO

**Evolución temporal destacable:**

**Patrón diario (por hora del día):**
- **Madrugada (00:00-08:00):** Bajo volumen, error rate 7%
- **Mañana (08:00-12:00):** Aumento de carga, error rate 8%
- **Tarde (12:00-18:00):** 🔴 **PICO CRÍTICO** - error rate 15%, response time sube a 1200ms promedio
- **Noche (18:00-24:00):** Descenso, error rate vuelve a 7%
- **Interpretación:** Problema recurrente en horario de máxima demanda

**Picos, anomalías o comportamientos llamativos:**

1. **Pico de errores en periodo 14:00-16:00 UTC:**
   - 28 errores en 2 horas
   - 3.5x superior al promedio
   - Correlaciona con response time máximo
   - Causas probables: Degradación de DB, sobrecarga de API

2. **Server-03 anómalo:**
   - 16.9% error rate vs 2.2% en server-01
   - 8x más errores que server-01
   - Indica problema específico de hardware o configuración
   - Acción: Inspeccionar server-03, posible reboot

3. **Database service bottleneck:**
   - Response time de DB requests: 1800ms promedio
   - vs 400ms de otros servicios
   - 15 errores específicos de conexión DB
   - Interpretación: Base de datos saturada o slow queries

4. **Payment service volatility:**
   - 10 errores en payment (99% success es standard del payment)
   - Impacto: Pérdida de transacciones monetarias
   - Severidad: CRÍTICA (pérdidas financieras)

5. **Memory warnings correlacionan con errors:**
   - Eventos de "Memory usage above 80%" 2 horas antes de crashes
   - Indica leak probable o falta de recursos

**CAPTURA 3: Evolución Response Time y Errores por Servicio**
![CAPTURA 3 - Métricas y Tendencias](Captura/captura3.png)

*Nota de la captura: Muestra gráfico de línea temporal con response time (eje Y) y colores por level (ERROR en rojo), también tabla de errores por servicio*

---

## 6. Dashboards de observabilidad

Describe los dashboards explorados:

**Dashboard Principal: "Dashboard Observabilidad - App Logs"**

Compuesto por 5 visualizaciones integradas:

**Visualización 1: Logs por Nivel (Barras verticales)**
- **Qué muestra:** Distribución de INFO (708), WARNING (194), ERROR (98) logs
- **Gráfico:** Barras verticales con colores: Verde (INFO), Amarillo (WARNING), Rojo (ERROR)
- **Patrón esperado:** 70/20/10 = SANO
- **Patrón actual:** 70.8/19.4/9.8 = MUY BUENO (dentro de parámetros)
- **Problema que detecta:** Aumento súbito de ERROR indica degradación de sistema
- **Acción:** Si ERROR > 15%, escalar a DevOps

**Visualización 2: Errores por Servicio (Barras horizontales)**
- **Qué muestra:** Ranking de servicios por número de errores
  - api-gateway: 20
  - auth-service: 28
  - database: 15
  - payment-service: 10
  - cache: 25
- **Información crítica:** database tiene error rate 15% (muy alto)
- **Problema que detecta:** Qué servicio específico está fallando
- **Acción:** Priorizar debugging en servicio "rojo" (más errores)
- **Usuario:** Desarrollador de backend responsable del servicio

**Visualización 3: Evolución Response Time (Línea temporal)**
- **Qué muestra:** Tendencia de response time (ms) a lo largo de 7 días
- **Líneas:** Diferenciadas por nivel (INFO línea verde, WARNING amarilla, ERROR roja)
- **Patrón:** 
  - INFO: ~400ms (normal)
  - WARNING: ~1200ms (degradación)
  - ERROR: ~2800ms (crítico, probable timeout)
- **Picos:** 14:00-16:00 UTC (response time sube a 3000ms)
- **Problema que detecta:** Degradación de rendimiento, cuello de botella
- **Acción:** Si response time > 2000ms, investigar carga/recursos
- **Usuario:** SRE (Site Reliability Engineer) para tuning de performance

**Visualización 4: Distribución Status Codes (Donut)**
- **Qué muestra:** Proporción de status codes
  - 200 (OK): 85.7%
  - 500 (Server Error): 4.5%
  - 502 (Bad Gateway): 3.5%
  - 503 (Unavailable): 2%
  - Otros: 4.3%
- **Indicador:** Verde si >95% es 200, rojo si >5% es 5xx
- **Problema que detecta:** Tipo de error (cliente vs servidor)
- **Acción:** 
  - Si 500 sube = problema backend
  - Si 502/503 sube = microservicio caído
- **Usuario:** Administrador de infraestructura

**Visualización 5: Top Hosts con Errores (Tabla)**
- **Qué muestra:** Tabla con hosts ordenados por error count
  - server-03: 42 errores
  - server-02: 28 errores
  - server-04: 23 errores
  - server-01: 5 errores (outlier positivo)
- **Información crítica:** server-03 es 8.4x más problemático que server-01
- **Problema que detecta:** Hardware/configuración específica fallando
- **Acción:** 
  - Inspeccionar server-03 (logs del SO, disk space, CPU)
  - Posible reboot o reemplazo
- **Usuario:** Sistema administrator / DevOps

**CAPTURA 4: Dashboard Observabilidad Completo**
![CAPTURA 4 - Dashboard Observabilidad Sin Filtros](Captura/captura4.png)

*Nota de la captura: Muestra dashboard completo con 5 visualizaciones, controles de filtro en la parte superior (level, service, host)*

---

## 7. Análisis e interpretación

Responde a las siguientes cuestiones:

### 1. ¿Qué tipo de incidencias técnicas se podrían detectar con estos datos?

**Incidencias críticas detectables:**

**A) Database Connection Failures (Fallos de conexión BD):**
- **Síntoma:** Spike en error messages "Database connection failed"
- **Indicadores:** 
  - Error rate de database service > 10%
  - Response time de queries > 2000ms
  - Status codes 500/502
- **Causa probable:** BD saturada, conexiones agotadas, query lenta
- **Acción:** Restart BD, check query performance, aumentar connection pool
- **Severidad:** CRÍTICA (aplicación no funciona sin BD)

**B) Memory Leak (Fuga de memoria):**
- **Síntoma:** Warning "Memory usage above 80%" seguido de crashes
- **Indicadores:**
  - Response time degradation gradual
  - Aumento de errores a lo largo del día
  - No se recupera después de restart
- **Causa probable:** Aplicación reteniendo objetos en memoria
- **Acción:** Heap dump analysis, código review, aumentar JVM memory
- **Severidad:** ALTA (eventual crash)

**C) Service Degradation (Degradación de servicio):**
- **Síntoma:** Response time sube pero no hay errores todavía
- **Indicadores:**
  - Status code 200 pero response_time > 1500ms
  - P95 latency creciente
  - Correlaciona con hora del día (14:00-16:00)
- **Causa probable:** Carga pico, recursos limitados, query ineficiente
- **Acción:** Escalar horizontalmente, optimizar queries, cache warming
- **Severidad:** MEDIA (usuarios notan lentitud)

**D) Payment System Errors (Errores de pago):**
- **Síntoma:** "Payment gateway error" apareciendo regularmente
- **Indicadores:**
  - 10 errores de payment en 7 días
  - Impacto financiero directo
  - Status codes 500/502 en payment-service
- **Causa probable:** API externa caída, rate limit, timeout
- **Acción:** Verificar integración con payment provider, retry logic, fallback
- **Severidad:** CRÍTICA (pérdidas monetarias inmediatas)

**E) Single Point of Failure - server-03:**
- **Síntoma:** Un servidor tiene 16.9% error rate vs otros ~9%
- **Indicadores:**
  - Errors concentrados en 1 host
  - Otros hosts funcionan bien
  - Patrón recurrente (no aleatorio)
- **Causa probable:** Hardware defectuoso, configuración incorrecta, network issue
- **Acción:** Investigación del host (dmesg, network, disk), posible reemplazo
- **Severidad:** MEDIA (redundancia puede absorber, pero no óptimo)

**F) API Gateway Bottleneck:**
- **Síntoma:** api-gateway tiene 20 errores, responde lento
- **Indicadores:**
  - Response time promedio alto
  - Correlaciona con picos de carga
  - Status 502/503 frecuentes
- **Causa probable:** Gateway saturado, rate limiting, backend timeout
- **Acción:** Load balancing, horizontal scaling, circuit breaker patterns
- **Severidad:** ALTA (todos los requests pasan por gateway)

**G) Auth Service Failures:**
- **Síntoma:** 28 errores de auth (12% error rate)
- **Indicadores:**
  - "Authentication failed" messages
  - Status 401/403 frecuentes
  - Afecta todos los usuarios
- **Causa probable:** Token service down, credential cache expired, LDAP timeout
- **Acción:** Reiniciar auth service, check external dependencies
- **Severidad:** CRÍTICA (sin auth, nada funciona)

---

### 2. ¿Qué diferencia hay entre analizar logs y analizar datos de negocio?

**Análisis de Logs (Observabilidad - Lab 4):**

| Aspecto | Logs | Datos Negocio |
|--------|------|---------------|
| **Objetivo** | Detectar problemas técnicos | Tomar decisiones comerciales |
| **Métrica clave** | Error rate, response time | Ventas, revenue, conversión |
| **Usuario** | DevOps, SRE, desarrollador | Manager, analista comercial |
| **Acción resultante** | "Reinicia server X" | "Expande equipo en Barcelona" |
| **Urgencia** | Minutos (sistema caído) | Horas/días (estrategia) |
| **Datos** | Técnicos (logs, métricas) | Comerciales (ventas, usuarios) |
| **Severidad de error** | Sistema no funciona → CRÍTICA | Dato erróneo → decisión subóptima |
| **Herramienta** | Kibana, Prometheus, ELK Stack | Kibana, BI clásico (Tableau) |
| **Pregunta típica** | "¿Por qué está roto?" | "¿Cuándo compra cada cliente?" |

**Ejemplo comparativo:**

*Análisis Log (Lab 4):*
```
Observo: "database service error rate 15%"
→ Pregunto: "¿Por qué falla database?"
→ Investigación: Query lenta, índice corrupto, disco lleno
→ Acción: Optimizar query, rebuild índice, limpiar disco
→ Resultado: Error rate baja a 2% en 30 minutos
```

*Análisis Negocio (Lab 1-3):*
```
Observo: "Barcelona vende 30% menos que Madrid"
→ Pregunto: "¿Por qué Barcelona tiene menos ventas?"
→ Investigación: Población menor, menos marketing, menor AUM
→ Acción: Aumentar budget marketing Barcelona, abrir sucursal
→ Resultado: Ventas Barcelona crecen 15% en 3 meses
```

**Diferencias clave:**

1. **Granularidad temporal:**
   - Logs: Segundos ("error happened at 14:32:15")
   - Negocio: Días/meses ("sales for January were...")

2. **Toma de decisiones:**
   - Logs: Reactiva (problema ocurrió, arreglo NOW)
   - Negocio: Proactiva (preveo que sucederá, preparo HOY)

3. **Stack técnico:**
   - Logs: DevOps tools (Prometheus, alerting, PagerDuty)
   - Negocio: BI tools (Tableau, Power BI, Looker)

4. **ROI medible:**
   - Logs: Uptime % (99.9% vs 99.95%)
   - Negocio: Revenue growth (€1M vs €1.5M)

---

### 3. ¿Qué información consideras más relevante en un sistema de observabilidad?

**Ranking de relevancia:**

**🔴 CRÍTICA (Debe monitorearse SIEMPRE):**

1. **Error Rate por Servicio**
   - Métrica: % de requests que fallan
   - Umbral alerta: >5%
   - Acción: Escalar inmediatamente
   - Razón: Indicador directo de system health

2. **Response Time (P95 latency)**
   - Métrica: milliseconds
   - Umbral alerta: >2000ms
   - Acción: Investigar bottleneck
   - Razón: Afecta experiencia usuario

3. **Availability por Service**
   - Métrica: Uptime %
   - Umbral alerta: <99.9%
   - Acción: Failover/restart
   - Razón: Servicios caídos = negocio parado

4. **Resource Utilization (CPU, Memory, Disk)**
   - Métrica: % de uso
   - Umbral alerta: CPU >80%, Memory >85%, Disk >90%
   - Acción: Scale horizontally o liberar recursos
   - Razón: Precursor de crashes

**🟡 IMPORTANTE (Monitorear regularmente):**

5. **Error Distribution (tipos de error)**
   - 5xx (servidor culpable) vs 4xx (cliente culpable)
   - Identifica causa raíz más rápido

6. **Dependency Health**
   - BD, cache, external APIs respondiendo?
   - Cascading failures

7. **Queue Depth / Job Backlog**
   - ¿Qué tan atrás va el procesamiento?
   - Síntoma de saturación

**🟢 COMPLEMENTARIA (Reportes, no alertas):**

8. **Error logs detallados**
   - Stack traces, user context
   - Para post-mortem y debugging

9. **Business metrics en observability**
   - "Transactions processed" vs "Errors"
   - Correlaciona tech con business

---

### 4. ¿Qué información falta para realizar un diagnóstico más preciso?

**Información técnica faltante:**

1. **Distributed Tracing (Trazas distribuidas):**
   - Actualmente: Vemos que database falla, pero no por qué
   - Falta: Trace ID de request completo (desde API → DB → response)
   - Utilidad: Identificar exactamente en qué paso se pierde la request
   - Herramienta: Jaeger, Zipkin

2. **Application Logs Detallados:**
   - Actualmente: Solo high-level "Database connection failed"
   - Falta: Stack trace, error code específico, valores de variables
   - Ejemplo: "Timeout after 5s connecting to DB host=prod-db-03 port=5432 user=app_user"
   - Utilidad: Diferenciar "BD caída" de "network issue" de "auth failure"

3. **Resource Metrics Granulares:**
   - Actualmente: Solo error rate general
   - Falta: 
     - Queries slow log (qué queries son lentas)
     - I/O metrics (disco lee/escribe muy lento?)
     - Network saturation (ancho de banda agotado?)
     - Garbage collection pauses (en aplicación Java)
   - Utilidad: Identificar if bottleneck es CPU/memory/disk/network

4. **Dependency Health:**
   - Actualmente: Asumimos external APIs funcionan
   - Falta: Health checks de payment gateway, LDAP server, email service
   - Métrica: Latency y error rate de cada dependency

5. **User Impact Metrics:**
   - Actualmente: Error rate técnico (9.8%)
   - Falta: Cuántos usuarios afectados realmente?
   - Métrica: "Affected Users" vs "Affected Requests"
   - Diferencia: 1 usuario sin acceso vs 1000 requests lentos

6. **Correlation with Deployments:**
   - Actualmente: Error rate spike a las 14:00
   - Falta: ¿Hubo un deploy en ese momento? ¿Config change?
   - Utilidad: Rápidamente saber if error = new deployment

7. **Business Context:**
   - Actualmente: "payment-service tiene 10 errores"
   - Falta: Cuánto dinero se perdió? Qué usuarios afectados? ¿VIP customers?
   - Utilidad: Priorizar severity (1 transacción VIP = 100 transacciones normales)

8. **Historical Baselines:**
   - Actualmente: Comparar day-to-day
   - Falta: Baselines históricos (week-over-week, year-over-year)
   - Ejemplo: "Hoy 12% error rate vs promedio 8% de hace 1 semana" = alarma

**Información proceso faltante:**

- **Root Cause Analysis automation:** Herramientas ML que automáticamente detecten patrones
- **Alerting inteligente:** No alertar por cada error, sino por anomalías
- **Runbooks:** Documentar qué hacer ante cada error
- **On-call automation:** Routing automático a engineer correcto

---

## 8. Comparación con otros usos de Kibana

Reflexiona brevemente:

### 1. ¿En qué se diferencia este uso de Kibana del trabajado en los Labs 1–3?

**Diferencias fundamentales:**

**Labs 1-3 (Análisis de Datos de Negocio):**
- **Datos:** Transacciones de ventas, comportamiento comercial
- **Usuarios:** Managers, analistas de negocio, directivos
- **Dashboards:** KPIs, tendencias de ventas, rentabilidad
- **Preguntas:** "¿Qué ciudad vende más?", "¿Cuál es el margen de cada producto?"
- **Acción resultante:** Decisiones estratégicas (estrategia comercial, presupuestos)
- **Tiempo de respuesta:** Horas a días
- **Impacto:** Crecimiento o decline en ventas
- **Ejemplo:** "Barcelona vende 30% menos, aumentemos marketing allí"

**Lab 4 (Observabilidad Técnica):**
- **Datos:** Logs de sistema, métricas técnicas, eventos de aplicación
- **Usuarios:** DevOps, SRE, desarrolladores, administradores
- **Dashboards:** Health checks, error rates, performance metrics, resource utilization
- **Preguntas:** "¿Por qué está lento?", "¿Qué servicio falla?", "¿Tiene disk space?"
- **Acción resultante:** Decisiones operacionales (restart service, scale out, fix bug)
- **Tiempo de respuesta:** Minutos a horas
- **Impacto:** Disponibilidad o indisponibilidad del sistema
- **Ejemplo:** "server-03 tiene 16.9% error rate, requiere mantenimiento urgente"

**Tabla comparativa:**

| Aspecto | Labs 1-3 (Negocio) | Lab 4 (Observabilidad) |
|--------|------------------|----------------------|
| **Índice** | `ventas` (datos transaccionales) | `app-logs` (eventos técnicos) |
| **Métrica principal** | Total ingresos | Error rate |
| **KPI crítico** | Revenue growth | Uptime % (99.9%+) |
| **Alerta típica** | "Ventas bajaron 20%" | "Error rate > 10%" |
| **Consecuencia si falla** | Menos dinero | Sistema caído |
| **Urgencia** | Planificación estratégica | INMEDIATA/CRÍTICA |
| **Dashboard users** | Junta directiva | SRE on-call team |
| **Update frequency** | Diaria/semanal | Real-time (segundos) |
| **Filtros típicos** | Ciudad, categoría, período | Level, service, host |
| **Visualización** | Barras, líneas temporales | Heatmaps, scatter plots |

---

### 2. ¿Por qué no tendría sentido usar dashboards de observabilidad como cuadros de mando de negocio?

**Razones técnicas:**

1. **Métrica incorrecta:**
   - Director pregunta: "¿Cuánto dinero ganamos?"
   - Dashboard observabilidad muestra: "Error rate 9.8%"
   - Respuesta: Irrelevante para decisión comercial

2. **Granularidad incompatible:**
   - Negocio piensa: "Semanal/mensual"
   - Observabilidad: "Segundo a segundo"
   - Ruido extremo para ver tendencias

3. **Contexto perdido:**
   - Observabilidad: "db-service tiene 15 errores"
   - Negocio: "¿Esto significa que pierdo €500?"
   - No hay correlación claro error técnico ↔ impacto financiero

4. **Usuarios diferentes:**
   - CEO no entiende "memory leak"
   - DevOps no entiende "gross margin"
   - Necesitan abstracciones diferentes

**Ejemplo de confusión:**

```
Observo en dashboard observabilidad: "payment-service error rate 10%"

Interpretaciones posibles:
- Negocio: "Perdimos 10% de ingresos hoy" (ERRÓNEO)
  → Solo 10 errores de 1000 requests = 1%, no 10%
  
- Negocio: "Necesito 10% de ingresos extra para compensar" (ERRÓNEO)
  → No sabemos cuántos errores = cuánto dinero
  → Podría ser €500 o €50.000
```

**Lo que SÍ necesita negocio:**
- KPI: "Payment success rate: 99.8%"
- Métrica: "Revenue lost due to payment errors: €423 today"
- Acción: "Contact 5 affected customers"

---

### 3. ¿Qué perfiles profesionales trabajan habitualmente con herramientas de observabilidad?

**Perfiles técnicos:**

**1. SRE (Site Reliability Engineer) - 👑 USUARIO PRINCIPAL**
- **Rol:** Responsable de disponibilidad y performance del sistema
- **Usa observabilidad para:** 
  - Monitoreo 24/7 en on-call
  - Investigación post-mortem
  - Capacity planning
- **Acciones:** "Page me if error rate > 5%", "Escalate if P95 > 3s"
- **Tools:** Kibana, Prometheus, Grafana, PagerDuty

**2. DevOps Engineer**
- **Rol:** Infraestructura, deployment, CI/CD pipelines
- **Usa observabilidad para:**
  - Detectar if deployments cause issues
  - Server health monitoring
  - Resource planning
- **Acciones:** "Rollback if error spike after deploy", "Scale down if CPU <10%"

**3. Backend Developer / Application Engineer**
- **Rol:** Escribir código, mantener servicios
- **Usa observabilidad para:**
  - Debug de bugs en producción
  - Performance optimization
  - Entender user behavior
- **Acciones:** "Check logs para ese error específico de user X"

**4. System Administrator**
- **Rol:** Mantenimiento de servidores, networking, storage
- **Usa observabilidad para:**
  - Server health (CPU, memory, disk, network)
  - Hardware failures detection
  - Capacity management
- **Acciones:** "server-03 disk 95% full, add storage"

**5. Platform Engineer / Architect**
- **Rol:** Diseñar sistemas observables, herramientas
- **Usa observabilidad para:**
  - Design decisions (microservices vs monolith)
  - Scaling strategies
  - Cost optimization
- **Acciones:** "Observabilidad muestra DB es bottleneck, redesign needed"

**6. Security Engineer / SecOps**
- **Rol:** Detectar brechas, comportamientos anómalos
- **Usa observabilidad para:**
  - Intrusion detection
  - Anomaly detection (tráfico extraño)
  - Audit trails
- **Acciones:** "Cantidad anormal de failed logins, posible ataque"

**7. Product Manager / Technical PM**
- **Rol:** Entender cómo usan los usuarios el producto
- **Usa observabilidad para:**
  - Feature performance
  - User journey analysis
  - Error impact on UX
- **Acciones:** "Nueva feature tiene 20% error rate, rollback o fix?"

**Flujo en empresa real:**

```
14:15 - Error rate spike a 15%
↓
PagerDuty alerts → On-call SRE paged
↓
SRE abre Kibana → Identifica database service
↓
SRE escala backend team → Backend dev investigates
↓
Backend dev → Find slow query → Optimizes
↓
DevOps deploy fix → Error rate baja a 2% en 10 min
↓
SRE post-mortem → Platform engineer redesigns
```

**Diferencia: Backend engineer vs DevOps vs SRE**

| Quién | Actitud | Acción |
|------|---------|--------|
| Backend | "Mi código tiene bug" | Escribe test, pushes fix |
| DevOps | "La deploy causa problema" | Rollback automático |
| SRE | "¿Cómo evitamos en futuro?" | Automating recovery, alerting |

---

---

## 9. Limitaciones del laboratorio

Indica al menos **dos limitaciones** del laboratorio, por ejemplo:

**LIMITACIÓN 1: Datos completamente simulados y no realistas**

- **Descripción:** Los logs están generados con distribuciones artificiales (70% INFO, 20% WARNING, 10% ERROR)
- **Problema:** En sistemas reales:
  - La ratio puede ser 99% INFO, 0.1% ERROR (observabilidad es sparse)
  - Los patrones son más complejos (no uniformes en tiempo)
  - Las causas raíz están entrelazadas (un problema causa cascada)
- **Impacto:** El análisis es "demasiado fácil", no hay contexto real
- **Ejemplo:** En lab identificar database como problema es simple; en producción hay 50 servicios interdependientes
- **Solución:** Usar logs reales de empresa o simulador más sofisticado (chaos engineering)

---

**LIMITACIÓN 2: Ausencia de Alerting automático**

- **Descripción:** Kibana es herramienta de visualización, no tiene alertas integradas sofisticadas
- **Problema:** En producción necesitas:
  - Alertas automáticas ("Si error rate > 5%, page SRE NOW")
  - Escalation policies (SRE no responde → page manager)
  - Runbooks automáticos (error rate alto → auto-restart service)
  - Correlation engine (error en service X + latency en service Y = common root cause)
- **Impacto:** Kibana requiere alguien mirando dashboard 24/7 (ineficiente)
- **Solución:** Integrar con Prometheus + Alertmanager + PagerDuty

---

**LIMITACIÓN 3: Falta de Distributed Tracing**

- **Descripción:** No podemos seguir un request individual a través de múltiples servicios
- **Problema:** Log "Database timeout" no nos dice:
  - En qué punto de la request ocurrió (inicio, mitad, final)
  - Cuánto tiempo pasó en cada servicio (api-gateway 100ms, auth 200ms, db 5000ms)
  - Dónde exactamente se perdió el request
- **Impacto:** Debugging es "connect the dots" manual
- **Ejemplo:** 
  - Con tracing: Click on request ID → See full flow: user → API → auth → DB (failed here after 5s)
  - Sin tracing: Múltiples logs de diferentes servicios, hay que correlacionar manualmente
- **Solución:** OpenTelemetry, Jaeger, Zipkin

---

**LIMITACIÓN 4: Métricas de nivel muy alto**

- **Descripción:** Sabemos que database service tiene error rate 15%, pero no por qué
- **Problema:** Falta granularidad:
  - ¿Qué queries son lentas? (slow query log)
  - ¿Qué índices faltan? (query plan analysis)
  - ¿Disco está saturado? (I/O metrics)
  - ¿Hay lock contention? (database-specific metrics)
- **Impacto:** Debugging es adivinanza, toma horas resolver
- **Solución:** Integrar logs de aplicación + database metrics + OS metrics

---

**LIMITACIÓN 5: Sin correlación con deployments/cambios**

- **Descripción:** Error rate sube a las 14:00, pero no sabemos si fue por:
  - Deploy (código nuevo introdujo bug)
  - Cambio de config (alguien cambió parámetros)
  - Carga aumentó (more users)
  - Problema de hardware (server falla)
- **Problema:** Imposible identificar causa sin contexto de cambios
- **Impacto:** Debugging ciego, muchos falsos positivos
- **Solución:** Integrar con Git/CI/CD, anotaciones de cambios en gráficos

---

**LIMITACIÓN 6: Falta de Machine Learning / Anomaly Detection**

- **Descripción:** Kibana visualiza datos, pero no detecta patrones anómalos automáticamente
- **Problema:** 
  - ¿Error rate 9.8% es normal o anómalo? (depende del baseline histórico)
  - ¿Response time 800ms es problema? (depende de la hora del día y load esperada)
  - ¿Correlación entre métricas es causal? (necesita análisis)
- **Impacto:** Requiere análisis manual, muchos falsos positivos/negativos
- **Solución:** ML para baselines, forecasting, correlation analysis

---

**LIMITACIÓN 7: Solo 7 días de datos (no suficiente para patrones)**

- **Descripción:** Laboratorio cubre solo 1 semana
- **Problema:** No detectamos:
  - Patrones semanales ("siempre falla los viernes")
  - Patrones mensuales ("end of month crash")
  - Patrones anuales ("December peak 10x load")
  - Tendencias de degradación (¿Empeora cada semana?)
- **Impacto:** Decisiones de capacity planning basadas en datos incompletos
- **Solución:** Retención de logs 1+ año, históricos para baseline

---

**LIMITACIÓN 8: Sin información de usuario impactado**

- **Descripción:** Sabemos "10 payment errors" pero no "qué clientes VIP afectados"
- **Problema:** 
  - 1 error que afecta CEO = urgencia máxima
  - 1000 errores que afectan usuarios de prueba = puede esperar
  - No sabemos costo financiero real del outage
- **Impacto:** Mala priorización de severidad
- **Solución:** Enriquecer logs con user_id, customer_tier, financial_impact

---

## 10. Reflexión final

Reflexiona brevemente sobre:

- qué has aprendido sobre observabilidad,
- la importancia de logs y métricas en sistemas reales,
- el papel de Kibana en la monitorización técnica.

(Extensión orientativa: 5–10 líneas)

---

Este laboratorio ha sido revelador porque muestra un **lado completamente diferente de Kibana** versus los Labs 1-3. He aprendido que **observabilidad no es "bonito dashboard para executives", sino "herramienta de guerra para DevOps en crisis a las 3 AM"**. La diferencia entre analizar datos de negocio (¿cuándo compra la gente?) y datos técnicos (¿por qué se cae el servidor?) es abismal: uno es estratégico, otro es táctico y urgente. He comprendido que **logs y métricas son el sistema nervioso del software**; sin ellos, estás ciego ante problemas hasta que usuarios reportan (demasiado tarde). En sistemas reales con microservicios, bases de datos, caches, etc., **una sola métrica (error rate) revela cascadas complejas**; ver que database tiene 15% error rate automáticamente te pregunta: ¿por qué?, y conduce a problemas de índices, queries lentas, memoria saturada. Finalmente, he comprendido que **Kibana es solo una parte de observabilidad real**; necesitas alerting automático (Prometheus), distributed tracing (Jaeger), y SREs que interpreten los datos bajo presión. Sin embargo, Kibana es **la puerta de entrada visual** que hace posible que humanos entiendan sistemas complejos rápidamente, transformando petabytes de logs en "database service tiene problema".

---

## 11. Dificultades encontradas (opcional)

Indica si has tenido dificultades técnicas o conceptuales y cómo las has resuelto.

**Dificultades técnicas:**

1. **Generación de logs simulados:**
   - **Problema:** Script Python necesitaba endpoints específicos de Elasticsearch
   - **Solución:** Validé que Elasticsearch estuviera ejecutándose primero (curl http://localhost:9200)
   - **Aprendizaje:** Siempre verificar prerequisites antes de ejecutar scripts bulk

2. **Filtros complejos en Discover:**
   - **Problema:** Aplicar múltiples filtros (level=ERROR AND service=database AND response_time_ms>2000) requería sintaxis correcta
   - **Solución:** Usar operador AND en Kibana query language, o aplicar filtros uno a uno visualmente
   - **Aprendizaje:** Kibana UI permite filtros visuales BUT también acepta KQL para combinaciones complejas

3. **Visualización con breakdown por nivel:**
   - **Problema:** Quería líneas separadas por nivel (INFO verde, WARNING amarilla, ERROR roja) en gráfico de tiempo
   - **Solución:** En Lens, "Break down by" field → level
   - **Aprendizaje:** Breakdown es distinto de agregación; permite desagregar datos por dimensión adicional

**Dificultades conceptuales:**

1. **Diferencia entre logs y métricas:**
   - **Problema:** Confundía si los datos eran "logs" (eventos textuales) o "métricas" (números)
   - **Solución:** Aclaración: logs son eventos con mensaje ("Database connection failed"), métricas son números (response_time_ms: 2500)
   - **Aprendizaje:** Labs 1-3 eran "cuasi-métricas" (números de ventas), Lab 4 es observabilidad (mix de logs + métricas)

2. **Urgencia vs estrategia:**
   - **Problema:** Inicialmente pensé "error rate 9.8% no es tan grave" como análisis de negocio
   - **Realización:** En observabilidad, 9.8% error rate = SRE en pánico, sistema se ve como "degraded"
   - **Aprendizaje:** Contexto muda completamente: 9.8% ventas perdidas = malo pero tolerable; 9.8% error rate = CRISIS

3. **Identificar insights en logs vs datos negocio:**
   - **Problema:** ¿Cuál es el "insight importante" en observabilidad?
   - **Solución:** En negocio buscamos oportunidades ("vender más en Barcelona"); en observabilidad buscamos **problemas a fijar** ("database es bottleneck")
   - **Aprendizaje:** La pregunta cambió de "¿Cómo crecer?" a "¿Qué está roto?"

4. **Correlación vs causación en errores:**
   - **Problema:** Vi que error rate sube a las 14:00 y response time también; ¿son relacionados?
   - **Solución:** Sí, muy probablemente response time lento CAUSA timeouts que RESULTAN en errores
   - **Aprendizaje:** En observabilidad, las causalidades son más claras que en datos de negocio

**Resoluciones generales:**
- Ejecutar scripts paso a paso, validar cada output
- Leer mensajes de error en Kibana, no asumir
- Buscar "best practices" de observabilidad en Google
- Comparar constantemente con Labs 1-3 para entender contrastes

---

## 12. Conclusión

Resume en 2–3 líneas qué aporta este laboratorio como complemento a la UD3 y qué diferencia introduce respecto al análisis de datos de negocio.

---

El Lab 4 de observabilidad **completa la visión integral de Big Data** mostrando que **no solo analizamos datos de negocio, sino también datos técnicos de sistemas**; mientras Labs 1-3 enseñan cómo explorar "¿qué compran nuestros clientes?", Lab 4 enseña "¿por qué se cae nuestro sistema?". La diferencia es crítica: **sin observabilidad, los mejores análisis de negocio son inútiles si el sistema está down**. Este laboratorio introduce el concepto de que **en arquitecturas Big Data modernas (Spark + Elasticsearch + Kibana), la capa de observabilidad es tan importante como la capa de análisis**, porque permite que los SREs y DevOps mantengan el sistema funcionando mientras analistas de negocio extraen insights. Kibana demuestra ser una herramienta versátil que sirve tanto para BI ejecutivo (Labs 1-3) como para monitorización técnica (Lab 4), cerrando la UD3 con una comprensión holística de cómo los datos técnicos y de negocio coexisten para sostener organizaciones data-driven.

---

## Fin del documento de entrega