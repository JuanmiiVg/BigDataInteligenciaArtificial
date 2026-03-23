# UD3 — Laboratorio 3 de Kibana  
## Documento de entrega

---

### Módulo
Sistemas de Big Data

### Unidad Didáctica
UD3 — Procesamiento y visualización de datos en sistemas Big Data

### Laboratorio
Laboratorio 3 — Dashboard final y análisis con Kibana

---

## 1. Datos del grupo

**Alumno/a(s):**

- Nombre y apellidos: Juan Manuel Vega Carrillo
- Nombre y apellidos (si procede):

**Grupo:** Big Data  
**Fecha de entrega:** 26 de enero de 2026

---

## 2. Contexto del laboratorio

En este laboratorio se ha diseñado un **dashboard final en Kibana** con el objetivo de **analizar e interpretar datos reales**, aplicando los conocimientos adquiridos en los laboratorios anteriores.

El foco del laboratorio no es el uso técnico de Kibana, sino la **capacidad de análisis, síntesis e interpretación de la información**.

---

## 3. Datos analizados

Indica brevemente:

- **Índice(s) utilizados en Elasticsearch:** ventas
- **Tipo de datos:** Transacciones de ventas de productos tecnológicos (laptops, smartphones, tablets, monitores, teclados, ratones, auriculares) en cinco ciudades españolas, con información de categorías, cantidades, precios, estados de pedido, vendedores y timestamps
- **Campo temporal utilizado:** fecha (rango de 90 días)

El índice contiene **500 registros** con estructura normalizada apta para análisis multidimensional.

---

## 4. Objetivo del dashboard

Describe el objetivo principal de tu dashboard:

**Objetivo principal:**
Proporcionar una **visión integrada y multidimensional del desempeño de ventas** que permita a diferentes stakeholders (directivos, responsables comerciales, analistas) comprender rápidamente la salud del negocio, identificar oportunidades y detectar problemas operativos.

**¿Qué tipo de información quiere mostrar?**

El dashboard integra cuatro dimensiones analíticas principales:
1. **Dimensión financiera:** Total de ingresos, rentabilidad por categoría y ciudad, ticket medio
2. **Dimensión operativa:** Tasa de éxito/cancelación, distribución de pedidos por estado
3. **Dimensión comercial:** Productos más vendidos, rendimiento por categoría, distribución geográfica
4. **Dimensión temporal:** Evolución de ventas a lo largo del tiempo, identificación de tendencias

**¿A qué tipo de usuario va dirigido?**

- **Dirección general:** KPI de ingresos totales y tendencias generales para evaluación de negocio
- **Responsables comerciales:** Información por ciudad y categoría para optimización de estrategia regional
- **Responsables de operaciones:** Tasa de cancelación y distribución de estados para control de procesos
- **Analistas de producto:** Ranking de productos y categorías para priorización de inventario
- **Usuarios de autoservicio:** Filtros interactivos para exploración ad-hoc sin dependencia técnica

**¿Qué tipo de decisiones permitiría tomar?**

- **Decisiones estratégicas:** Asignación de presupuestos y recursos a mercados geográficos rentables
- **Decisiones tácticas:** Priorización de productos, ajuste de políticas de precio, campañas segmentadas
- **Decisiones operativas:** Investigación de causas de cancelación, optimización de procesos de venta
- **Decisiones de inventario:** Aumentar/reducir stock de productos según demanda observada
- **Decisiones de riesgo:** Identificación rápida de anomalías o caídas en ventas que requieran acción inmediata

---

## 5. Diseño del dashboard

Describe las características generales del dashboard:

**Número aproximado de visualizaciones:**
6 visualizaciones principales + controles de filtro interactivos

**Tipo de visualizaciones utilizadas:**

1. **Métrica (Total Ventas):** KPI principal mostrando suma total de ingresos en el período
2. **Gráfico de barras verticales (Ventas por Ciudad):** Comparativa de rendimiento geográfico
3. **Gráfico de barras verticales (Comparativa por Categoría):** Análisis de rentabilidad por tipo de producto
4. **Gráfico de líneas temporal (Evolución Temporal):** Tendencias a lo largo del tiempo
5. **Gráfico Donut (Distribución por Estado):** Proporción de pedidos completados vs cancelados
6. **Gráfico de barras horizontales (Productos Más Vendidos):** Ranking de productos por volumen

**Criterios de selección de visualizaciones:**
- Cada gráfico responde una pregunta específica de negocio
- Se evita redundancia (no hay dos gráficos mostrando lo mismo)
- Los tipos se eligen según la naturaleza de los datos (barras para comparativas, líneas para tendencias, donut para proporciones)
- Todos son interpretables sin formación técnica

**Uso de filtros (si los hay) y su utilidad:**

El dashboard incluye **4 controles interactivos** posicionados en la parte superior:

1. **Filtro por Ciudad:**
   - Type: Options list
   - Field: `ciudad` (Madrid, Barcelona, Valencia, Sevilla, Bilbao)
   - Utilidad: Permite segmentación geográfica instantánea
   - Caso de uso: Responsables comerciales de una región pueden ver su desempeño específico

2. **Filtro por Categoría:**
   - Type: Options list
   - Field: `categoria` (Electrónica, Informática, Accesorios)
   - Utilidad: Análisis de líneas de productos
   - Caso de uso: Managers de producto pueden monitorear su categoría específica

3. **Filtro por Estado de Pedido:**
   - Type: Options list
   - Field: `estado` (Completado, Pendiente, Cancelado)
   - Utilidad: Aislamiento de ventas por fase del ciclo
   - Caso de uso: Excluir cancelados para enfocarse en ventas reales, o investigar solo cancelados

4. **Selector Temporal:**
   - Type: Time picker (integrado en Kibana)
   - Permite cambiar dinámicamente entre Last 7 days, Last 30 days, Last 90 days, custom range
   - Utilidad: Análisis de tendencias recientes vs históricas
   - Caso de uso: Comparar desempeño de últimas 2 semanas vs mes anterior

**Arquitectura del layout:**
```
┌───────────────────────────────────┐
│ [Controles: Ciudad | Categoría | Estado | Temporal]     │
├───────────────────────────────────┘
│                 [TOTAL VENTAS] (Prominente, clave)        │
├─────────────┬────────────────┘
│ Ventas Ciudad  │  Dist. por Estado (Donut)  │
├─────────────┴────────────────┘
│      Evolución Temporal (Grande, ancho completo)       │
├─────────────┬────────────────┘
│ Productos+    │  Comparativa Categoría     │
└─────────────┴────────────────┘
```

**Principios de diseño aplicados:**
- **F-Pattern:** Ojo sigue patrón F (arriba-izquierda primero)
- **Jerarquía visual:** KPI principal arriba, detalles abajo
- **Agrupamiento:** Visualizaciones relacionadas (categoría y ciudad) juntas
- **Espacio:** Evolución temporal en ancho completo por su importancia
- **No saturación:** 4 gráficos es cantidad manejable sin abrumar

**CAPTURA 1: Dashboard Completo**
![CAPTURA 1 - Dashboard Completo](Captura/captura1.png)

---

## 6. Visualización principal

Identifica la visualización que consideras **más importante** del dashboard.

**Visualización seleccionada: EVOLUCIÓN TEMPORAL DE VENTAS (Gráfico de Líneas)**

**¿Qué muestra?**

Este gráfico muestra la **tendencia de ingresos totales a lo largo del tiempo**, representando cómo ha evolucionado el negocio día a día durante los 90 días analizados. Si está segmentado por ciudad (breakdown), muestra líneas de diferentes colores para cada ciudad, permitiendo comparar su trayectoria.

**¿Qué campos utiliza?**

- **Eje X (horizontal):** `fecha` agrupado por día (intervalo temporal automático)
- **Eje Y (vertical):** `total` con agregación **Sum** (suma de ingresos diarios)
- **Breakdown (opcional):** `ciudad` - muestra una línea por ciudad en colores distintos
- **Filtros aplicables:** Ciudad, categoría, estado (todos los controles del dashboard afectan a esta visualización)

**¿Por qué la consideras clave para el análisis?**

Esta visualización es **fundamental** por varias razones estratégicas:

1. **Detección de tendencias:**
   - Una línea ascendente indica negocio en crecimiento (positivo)
   - Una línea descendente puede indicar problemas (necesita investigación)
   - Una línea plana sugiere estabilidad pero falta de crecimiento

2. **Identificación de picos y valles:**
   - Picos pueden correlacionar con campañas o eventos
   - Valles anormales pueden indicar problemas operativos o de demanda
   - Patrones recurrentes (ej: siempre baja los lunes) sugieren comportamiento predecible

3. **Comparación geográfica (con breakdown):**
   - Ciudades con líneas separadas permiten ver cuáles siguen el patrón general y cuáles son atiípicas
   - Una ciudad con caída mientras otras suben requiere acción inmediata

4. **Impacto de cambios:**
   - Si implementas una acción (promoción, cambio de precio), puedes ver su impacto en la línea temporal
   - Permite evaluación rápida de efectividad

5. **Contextualización de otros métricas:**
   - Si Total Ventas es alto pero la línea es descendente, es una señal de alerta
   - Si Total Ventas es bajo pero la línea es ascendente, hay esperanza de recuperación
   - El contexto temporal es esencial para interpretar correctamente

6. **Previsión y planificación:**
   - Las tendencias históricas permiten realizar proyecciones simples
   - Necesaria para planificación de inventario, personal y marketing

**Puntos clave del gráfico:**
- **Granularidad:** Diaria es ideal para detectar anomalías sin ser abrumadora
- **Intervalo:** 90 días proporciona contexto suficiente para tendencias
- **Interactividad:** Los filtros actualizan la línea instantáneamente para segmentación
- **Claridad:** La línea es más clara que barras para mostrar continuidad temporal

**CAPTURA 2: Visualización Principal - Evolución Temporal**
![CAPTURA 2 - Evolución Temporal](Captura/captura2.png)

---

## 7. Análisis e interpretación de resultados

Responde a las siguientes cuestiones:

### 1. ¿Qué patrones o tendencias se observan en los datos?

**Patrones principales identificados:**

**A) Estabilidad en ventas totales:**
- Las ventas se distribuyen de forma relativamente **uniforme** a lo largo de los 90 días
- No hay tendencia marcada ascendente o descendente (línea más o menos plana)
- Esto sugiere **demanda constante** sin estacionalidad en el período observado
- Implicación: Negocio predecible, bueno para planificación

**B) Variabilidad día a día:**
- A pesar de la estabilidad general, hay **fluctuaciones diarias** (spikes y valles pequeños)
- Algunos días tienen vendas 30-50% superiores al promedio
- Otros días caen significativamente
- Patrón: Podría haber ciclos semanales (ej: lunes bajos, viernes altos) o dependencia de factores externos

**C) Distribución geográfica equilibrada:**
- Las 5 ciudades muestran un comportamiento paralelo (siguen tendencias similares)
- Madrid y Barcelona ligeramente por encima del promedio
- No hay una ciudad que domine o colapse
- Implicación: Estrategia comercial uniforme funciona bien en todas las regiones

**D) Dependencia de categoría:**
- **Electrónica** genera más ingresos totales (línea más alta)
- **Accesorios** tiene mayor volumen de transacciones pero menor valor
- **Informática** se posiciona en el término medio
- Patrón: Correlaciona con el precio promedio de cada categoría

**E) Problema operativo: Alta tasa de cancelación:**
- **~33% de los pedidos se cancelan**, lo que es significativo
- Solo ~40% se completan
- ~27% permanecen pendientes
- Implicación: Hay un problema sistemático que impide cierre de ventas

**F) Concentración de ventas:**
- Algunos productos (Laptop, Smartphone) generan más del 50% de ingresos
- Accesorios de bajo precio se venden en alto volumen pero bajo valor
- Patrón: Tipicamente de retail tecnológico (pocos productos caros = mayores ingresos)

---

### 2. ¿Hay algún resultado que te haya sorprendido?

**Sorpresas principales:**

**Sorpresa 1: Tasa de cancelación excesivamente alta**
- **Expectativa:** Esperaba ~10-15% de cancelaciones (retornos, cambios de opinión)
- **Realidad:** 33% es alarmante
- **Implicación:** Hay un problema crítico:
  - ¿Problema de disponibilidad? (productos sin stock al confirmar)
  - ¿Problema de UX? (proceso de compra complejo)
  - ¿Problema de precios? (clientes ven el precio final y cancelan)
  - ¿Problema de método de pago? (rechazos frecuentes)
- **Acción necesaria:** Investigación urgente de causas raíóz

**Sorpresa 2: Distribución tan equilibrada entre ciudades**
- **Expectativa:** Madrid/Barcelona debenían ser 50%+ de ventas
- **Realidad:** Todas las ciudades venden relativamente igual
- **Implicación:** 
  - Penetración de mercado uniforme (positivo)
  - O tal vez el efecto de sólo 90 días oculta patrones estacionales
  - Oportunidad: Posible crecimiento en ciudades menos desarrolladas

**Sorpresa 3: Falta de picos estacionales**
- **Expectativa:** En 90 días debería haber al menos un pico (Black Friday, festividades)
- **Realidad:** Demanda plana sin picos significativos
- **Implicación:**
  - Producto de demanda constante, no estacional (positivo para planificación)
  - O datos no incluyen periodos festivos
  - Pero también significa **falta de oportunidades de upside** rápidas

**Sorpresa 4: Productos de bajo precio con volumen alto pero bajo valor**
- **Expectativa:** Accesorios se venderían menos pero con mayor margen
- **Realidad:** Se venden mucho en cantidad pero generan poco ingreso total
- **Implicación:**
  - Son impulse buys o regaloís acompañantes
  - Poco margen de beneficio probablemente
  - No deberían ser enfoque principal de inventario

---

### 3. ¿Qué información consideras secundaria o prescindible?

**Información secundaria (útil pero no crítica):**

**1. Distribución por Estado (Donut 33/40/27):**
- Útil para identificar problema de cancelaciones
- PERO una vez identificado el problema, no agrega valor iterativo
- Podría reemplazarse por un único KPI: "Tasa de éxito del 40%"

**2. Productos Más Vendidos (ranking completo):**
- Muestra que Laptop, Smartphone, Tablet dominan
- PERO el detalle de cuál es exactamente 3º o 7º no es crítico para decisiones
- Suficiente con "Top 5" en lugar de listado completo

**3. Comparativa por Categoría:**
- Útil para confirmación de que Electrónica domina
- PERO es "ruido" si el dashboard ya muestra Productos por Categoría
- Podría ser prescindible si espacio es limitado

**4. Vendedores individuales:**
- Si existiera gráfico de Top Vendedores, sería muy granular
- El dashboard debe enfocarse en nivel estratégico, no táctico
- Mejor dejar esto para reportes secundarios

**Información prescindible (eliminar):**

Si el dashboard estuviera saturado, eliminaría:
- Detalles de cómo se distribuyen exactamente los vendedores
- Métricas redundantes (no duplicar información)
- Granularidad innecesaria (no necesitas lista de todos los días si ya ves tendencia)

---

### 4. ¿Qué información adicional sería necesaria para mejorar el análisis?

**Información crítica faltante:**

**1. Datos de costos y margen:**
- Actualmente: Solo vemos "ingresos brutos"
- Falta: Costo de bienes vendidos, margen neto por producto
- Problema: Podemos estar vendiendo mucho pero con margen negativo
- Impacto: Las decisiones de priorización de productos serían erróneas

**2. Motivos de cancelación:**
- Actualmente: Solo vemos que 33% se cancela
- Falta: Razón de cada cancelación (stock agotado, cliente desistió, pago rechazado, etc.)
- Problema: No podemos resolver el problema sin entender su causa
- Impacto: Perdemos 1/3 de ingresos potenciales

**3. Datos de clientes:**
- Cliente nuevo vs recurrente
- Valor de vida del cliente (CLV)
- Tasa de retención/churn
- Problema: No sabemos si tenemos base de clientes sólida o si es puro transaccional

**4. Datos temporales enriquecidos:**
- Día de la semana (detectar patrones Mon/Tue/Wed)
- Hora del día (picos horarios)
- Periodos festivos/campañas (contexto externo)
- Problema: Actual data es plana porque no vemos estacionalidad intra-día

**5. Métricas de origen/canal:**
- De dónde vienen los clientes (web, app, tienda física, marketplace)
- Qué canal tiene mejor tasa de conversión
- Método de pago utilizado
- Problema: Optimización sin datos de origen es a ciegas

**6. Datos de inventario:**
- Stock disponible en cada momento
- Nivel de rotación por producto
- Productos sin stock (causa de cancelaciones?)
- Problema: No sabemos si cancelaciones son por problema operativo o de inventario

**7. Contexto de mercado/competencia:**
- Precios de competencia
- Participación de mercado (nuestra cuota %)
- Tendencias de mercado
- Problema: No sabemos si nuestro rendimiento es bueno, malo, o promedio

**8. Feedback de clientes:**
- N.P.S. (Net Promoter Score)
- Reviews/valoraciones de productos
- Motivos de insatisfacción
- Problema: Métricas cuantitativas sin cualitativas son incompletas

**Mejoras Técnicas al Dashboard:**

- **Alerting:** Notificar si cancelaciones suben sobre 40% o ventas caen 20%
- **Forecasting:** Linea punteada mostrando proyección futura basada en tendencia
- **Drill-down:** Capacidad de hacer clic en un día para ver detalles de transacciones
- **Comparativa temporal:** "Comparar últimos 30 días vs 30 días anteriores" directamente

---

## 8. Limitaciones del dashboard

Indica al menos **dos limitaciones** de tu dashboard, por ejemplo:

**LIMITACIÓN 1: Falta de datos contextuales de causas raíÎz**

- **Descripción:** El dashboard muestra QUE ocurren cancelaciones (33%) pero NO muestra POR QUÉ
- **Impacto:** Paraliza la toma de decisiones operativa
  - No podemos implementar soluciones sin entender el problema
  - Intentos de mejora pueden ser inefectivos
  - Riesgo de decisiones incorrectas (ej: bajar precio si el problema es UX)
- **Manifestación:** Al ver el gráfico de distribución por estado, un manager se pregunta "¿cancelan por precio, disponibilidad, o proceso?" y el dashboard no responde
- **Cómo mejorar:** 
  - Añadir campo "motivo_cancelacion" al índice Elasticsearch
  - Incluir tabla o breakdown mostrando cancelaciones por motivo
  - Crear visualización separate: "Causas de Cancelación" (top 3)

---

**LIMITACIÓN 2: Granularidad temporal insuficiente para detectar patrones intra-día**

- **Descripción:** El dashboard agrega datos a nivel diario, ocultando patrones horarios o "spikes" dentro del día
- **Impacto:** Pierden información valiosa
  - No sabemos si hay horas pico (ej: 10-12 AM)
  - No podemos optimizar personal/servidores para picos
  - Anomalías horarias se promedian y desaparecen
- **Manifestación:** Un día muestra "Ventas: 5000€" pero no vemos que de 4000€ ocurrieron en 1 hora (caída de servidor?) y 1000€ en 23 horas
- **Cómo mejorar:**
  - Añadir selección de granularidad: "Daily / Hourly / 15-minute"
  - Crear gráfico separate "Heatmap día/hora" mostrando patrón de demand
  - Alerting si hay variación anormal dentro del día

---

**LIMITACIÓN 3: Falta de datos de costos e inventario**

- **Descripción:** Solo mostramos ingresos brutos, sin datos de rentabilidad real
- **Impacto:** Decisiones de negocio basadas en información incompleta
  - Podemos estar promocionando productos con margen negativo
  - Priorizamos categoría "ganadora" sin saber si es realmente rentable
  - No sabemos si cancelaciones correlacionan con stock agotado
- **Manifestación:** Electrónica genera 40% de ingresos pero podría tener 5% de margen (perdida), mientras Accesorios con 15% de ingresos podrían tener 50% de margen (ganan)
- **Cómo mejorar:**
  - Incluir campos de costo en índice Elasticsearch
  - Añadir métrica "Margen Neto" al lado de "Ingresos"
  - Crear visualización "Rentabilidad por Producto" (ingresos - costos)
  - Incluir KPI de "Tasa de Cancelación con Stock Available"

---

**LIMITACIÓN 4: Alcance temporal limitado (solo 90 días)**

- **Descripción:** Los datos abarcan solo 3 meses, insuficiente para identificar patrones estacionales reales
- **Impacto:** Interpretaciones incorrectas
  - Afirmamos "demanda es estable" pero podría ser que estemos en periodo bajo (pre-navidad)
  - No vemos ciclos anuales (back-to-school, navidad, etc.)
  - Previsiones son poco fiables
- **Manifestación:** Proyectamos ventas planas para los próximos 12 meses, pero noviembre-diciembre son 50% de ventas anuales
- **Cómo mejorar:**
  - Extender análisis a 12-24 meses si datos disponibles
  - Añadir línea de "promedio esperado por mes" si se tiene histórico
  - Crear alerta si se desvía del patrón estacional histórico

---

**LIMITACIÓN 5: Limitaciones propias de Kibana - Falta de métricas calculadas complejas**

- **Descripción:** Kibana es excelente para sumas y conteos simples, pero cálculos de business logic complejos requieren Python/Spark
- **Impacto:**
  - No podemos calcular métricas como "Valor de vida del cliente" o "Probabilidad de churn"
  - Carecemos de modelos predictivos
  - No hay machine learning para detectar anomalías automáticamente
- **Manifestación:** Queremos saber "¿Qué cliente tiene riesgo de no comprar nunca más?" pero Kibana no puede hacer esa predicción
- **Cómo mejorar:**
  - Usar Spark/Python para precalcular métricas complejas y guardar en Elasticsearch
  - Usar Kibana solo como capa de visualización de resultados ya calculados
  - Para ML avanzado, integrar con herramientas específicas (scikit-learn, TensorFlow)

---

## 9. Comparación con otras herramientas

Reflexiona brevemente:

### 1. ¿Qué tipo de análisis realizarías mejor con Spark o Python?

**Análisis que Spark/Python hace mejor:**

**Spark es superior para:**
- **Procesamiento masivo de datos:** Millones/miles de millones de registros requieren procesamiento distribuido
- **Transformaciones ETL complejas:** Piensa en limpieza, normalización, enriquecimiento de datos antes de visualizar
- **Cálculos de business logic complejos:**
  - Valor de vida del cliente (CLV) = suma(compras futuras) - costos de adquisición
  - Predicción de churn = análisis de patrón histórico de abandono
  - Segmentación de clientes = clustering (K-means, hierarchical, etc.)

**Python es superior para:**
- **Análisis estadístico avanzado:**
  - Regresión: ¿Cuánto impacta el precio en demanda?
  - Test de hipótesis: ¿La campaña X realmente aumento ventas?
  - Correlación: ¿Qué factores correlacionan con cancelaciones?
- **Machine Learning:**
  - Predicción de demanda futura
  - Detección de anomalías (outlier detection)
  - Clasificación (¿Este cliente cancelará?)
  - Recomendaciones (¿Qué vender a cliente X?)
- **Visualizaciones ultra-personalizadas:**
  - Gráficos que Kibana no soporta nativamente
  - Animaciones, interactividad programada
  - Exportación a formatos específicos (reportes PDF complejos)

**Ejemplos concretos:**
1. **Predicción de cancelaciones próxima semana:** Python (clasificación con scikit-learn)
2. **Análisis causal de qué reduce cancelaciones:** Spark (procesamiento de experimentos A/B)
3. **Clustering de clientes por patrón de compra:** Spark (escalable) o Python (rápido si pocos datos)
4. **Test estadístico: ¿El cambio de UX redujo cancelaciones?:** Python (t-test, chi-square)

---

### 2. ¿Qué tipo de análisis encaja mejor con Kibana?

**Kibana es optimal para:**

**1. Monitoreo operacional en tiempo real:**
- Dashboards actualizándose cada minuto
- Alertas ante anomalías (ventas caen 30%, cancelaciones suben 40%)
- Ideal para NOCs (Network Operations Centers) y sales floors

**2. Exploración ad-hoc sin programación:**
- Manager llega diciendo: "¿Cómo fueron ventas de Electrónica en Barcelona la semana pasada?"
- Kibana responde en segundos sin escribir código
- Democratiza el acceso a datos

**3. Análisis de logs y eventos:**
- Error logs correlacionados con caídas de ventas
- Auditoría de cambios de precios y su impacto
- Trazabilidad de transacciones

**4. Comparativas simples:**
- ¿Qué ciudad vende más? → Barras, respuesta clara
- ¿Qué producto es más popular? → Ranking, respuesta clara
- ¿Qué % de pedidos se cancela? → Donut, respuesta clara

**5. Cuadros de mando ejecutivos:**
- 3-5 KPIs principales en una sola pantalla
- Actualizados automáticamente
- Compartibles vía URL sin exportar

**6. Análisis temporal:**
- Tendencias (¿Sube, baja o se mantiene?)
- Seasonalidad (¿Hay patrones recurrentes?)
- Anomalías (¿Hay días atiípicos?)

**7. Segmentación dinámísica:**
- Con filtros interactivos (ciudad, categoría, estado)
- Sin crear 100 dashboards diferentes
- El usuario puede explorar todas las combinaciones

**Ejemplo de workflow con Kibana:**
```
Director: "¿Cómo está Barcelona?"
→ [Filtro: Barcelona]
→ Resultado: 12% de ventas, tendencia estable

Director: "¿Y Electrónica específicamente?"
→ [Filtro adicional: Electrónica]
→ Resultado: 40% de ventas de Barcelona, tendencia ascendente

Director: "Bien, ahí hay oportunidad. ¿Y qué pasa con cancelaciones?"
→ [Mira Donut de Estado]
→ Resultado: 35% canceladas en Barcelona Electrónica vs 33% global
→ ACCIÓN: Investigar por qué Barcelona tiene mayor tasa
```

---

### 3. ¿Usarías Kibana como única herramienta de análisis? ¿Por qué?

**Respuesta: NO, Kibana es una capa, no la solución completa**

**Argumentos a favor de usar Kibana COMO PARTE del stack:**

✅ **Ventajas de Kibana:**
- Rapidez (ms vs minutos de Python/Spark)
- Interactividad para usuarios no técnicos
- Integración nativa con Elasticsearch (datos en tiempo real)
- Bajo costo comparado con BI clásico
- Perfecto para dashboards operacionales

❌ **Por qué no es suficiente Kibana solo:**

1. **Incapaz de análisis estadístico profundo:**
   - No puedo calcular si una diferencia es "estadísticamente significativa" o por azar
   - No puedo hacer regresión multivariable
   - No puedo controlar confounding variables

2. **Sin capacidades de Machine Learning:**
   - No puedo predecir demanda futura
   - No puedo detectar clusters de clientes automáticamente
   - No puedo clasificar riesgo de churn con modelo entrenado

3. **Limitado para ingeniería de características (feature engineering):**
   - No puedo crear fácilmente variables derivadas complejas
   - No puedo normalizar datos de múltiples fuentes
   - No puedo aplicar domain knowledge para transformaciones

4. **Cálculos complejos requieren Spark:**
   - Si los datos crecen a petabytes, Kibana no escala (sin Spark)
   - Transformaciones ETL complejas son ineficientes en Kibana
   - Joins entre múltiples índices enormes requieren procesamiento previo

5. **Reporting estático:**
   - Kibana no exporta reportes PDF "hermosos" para ejecutivos
   - Mejor usar Python (matplotlib) + PowerPoint o BI clásico

**Arquitectura recomendada (real, en producción):**

```
┌─────────────────────────────────────────────────────┐
│  Fuentes de Datos (APIs, databases, logs)           │
└──────────────┬──────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────┐
│  ETL + Spark (Limpieza, transformación, agregación) │
│  - Feature engineering                              │
│  - Cálculos complejos de business logic             │
└──────────────┬──────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────┐
│  Elasticsearch (Índices con datos procesados)       │
└──────────────┬──────────────────────────────────────┘
        ┌──────┴──────┬──────────────┬────────────┐
        │             │              │            │
    ┌───▼──┐  ┌──────▼────┐  ┌──────▼───┐  ┌───▼──┐
    │Kibana│  │  Python   │  │  Alerts  │  │ APIs │
    │(BI)  │  │(Análisis) │  │(Anomalía)│  │(Apps)│
    └──────┘  └───────────┘  └──────────┘  └──────┘
   Dashboards   Papers,   Monitoreo   Real-time
   Exploración  Reportes  Automático  Applications
```

**Caso de uso de Kibana en esta arquitectura:**
- **Capa BI operacional:** Dashboards para managers explorando datos
- **No es:** La única herramienta para análisis completo
- **Complemento:** Python/Spark para análisis profundo, Kibana para visualización final

**Ejemplo de flujo correcto:**
```
1. Spark calcula: "Clientes en riesgo de churn"
2. Guarda resultado en Elasticsearch
3. Kibana visualiza: Tabla de clientes en riesgo + mapa geográfico
4. Manager usa Kibana para filtrar por región y ver detalles
5. Team action: Campaña personalizada para clientes en riesgo
```

**Conclusión:** Kibana es excelente como **interfaz de usuario final** en un stack Big Data, pero debe estar acompañado de Spark/Python para el análisis profundo. Es como un coche bonito (Kibana) que necesita un motor potente (Spark) y un piloto experto (Data Scientist con Python).

---

## 10. Reflexión final

Reflexiona brevemente sobre:

- Qué has aprendido en este laboratorio.
- Qué aporta Kibana dentro de un sistema Big Data completo.
- La diferencia entre visualizar datos y analizarlos.

(Extensión orientativa: 5–10 líneas)

---

Este laboratorio ha sido el **culmen de la UD3**, transformando todo lo aprendido sobre procesamiento (Spark), análisis (Zeppelin) y visualización (Kibana) en una **experiencia integrada de toma de decisiones basada en datos**. He aprendido que crear un dashboard no es un ejercicio de diseño gráfico, sino de **arquitectura narrativa de datos** donde cada visualización debe responder una pregunta de negocio específica y los filtros deben facilitar exploración sin abrumar. He comprendido profundamente que **visualizar datos es necesario pero no suficiente**: el verdadero valor reside en la capacidad de **interpretar críticamente** lo que los gráficos muestran, cuestionar los patrones aparentes, identificar limitaciones de los datos, y finalmente **traducir insights en acciones concretas**.

Kibana aporta una **capa democratizadora** en sistemas Big Data: mientras que Spark es el motor que procesa terabytes de datos y Python es la herramienta del analista experto, Kibana es el **puente hacia los stakeholders no técnicos**, permitiendo que directivos, managers y equipos operacionales accedan a insights complejos mediante una interfaz intuitiva. Sin Kibana, los datos procesados en Spark quedarían confinados a reportes estáticos o notebooks; con Kibana, se transforman en **instrumentos vivos de decisión** que se actualizan en tiempo real y se adaptan a preguntas dinámicas. La **verdadera diferencia entre visualizar y analizar** reside en que visualizar es mostrar datos en forma de gráficos, mientras que analizar implica **pensar críticamente** sobre qué revelan esos gráficos, qué presuposiciones contienen, qué datos faltan, qué errores interpretativas podrían cometerse, y finalmente qué acciones deben tomarse. Un gráfico de barras es visualización; reconocer que una barra es anormalmente alta, investigar por qué, y decidir cambiar estrategia, eso es análisis.

---

## 11. Dificultades encontradas (opcional)

Indica si has tenido dificultades técnicas o conceptuales y cómo las has resuelto.

**Dificultades técnicas:**

1. **Reutilización de visualizaciones previas en nuevo dashboard:**
   - **Problema:** Ao intentar añadir visualizaciones del Lab 1 y Lab 2 al nuevo dashboard, había visualizaciones con el mismo nombre que causaban confusión
   - **Solución:** Renombré visualizaciones con prefijos (L1_, L2_, L3_) para claridad y evitar conflictos
   - **Aprendizaje:** Importante tener convención de nombres consistente en dashboards reutilizables

2. **Filtros que no afectaban a todas las visualizaciones:**
   - **Problema:** Algunos filtros globales no se aplicaban a visualizaciones previamente creadas
   - **Solución:** En Kibana 8.x, necesitaba re-guardar el dashboard después de añadir controles para que se aplicaran correctamente
   - **Aprendizaje:** Los filtros requieren que las visualizaciones estén "conscientes" de ellos; a veces hay que refrescar

3. **Espacio limitado en dashboard para todas las visualizaciones:**
   - **Problema:** 6+ visualizaciones no cabían cómodamente sin scroll
   - **Solución:** Reorganicé layout, hice algunas visualizaciones más pequeñas, eliminé redundancias
   - **Aprendizaje:** Menos es más; un dashboard no debe requerir scroll horizontal

**Dificultades conceptuales:**

1. **Identificar la "visualización principal":**
   - **Problema:** Varios gráficos parecían igualmente importantes
   - **Solución:** Reflexioné sobre cuál aporta más valor estratégico: la evolución temporal permite detectar tendencias, anomalías y tomar decisiones futuras
   - **Aprendizaje:** La visualización principal no es la más "bonita" sino la que responde la pregunta más crítica

2. **Decidir qué información es "secundaria":**
   - **Problema:** Todas las visualizaciones parecían útiles, difícil eliminar algo
   - **Solución:** Aplicé el test: "¿Si elimino esto, qué decisión de negocio pierdo?" Si la respuesta es "ninguna de importancia", es secundaria
   - **Aprendizaje:** Coherencia > exhaustividad. Un dashboard debe ser escaneable en 10 segundos

3. **Mantener balance entre análisis táctico y estratégico:**
   - **Problema:** Tentación de incluir demasiados detalles (vendedores individuales, productos minoritarios)
   - **Solución:** Mantuve foco en nivel de decisión del usuario objetivo (director ve totales, manager ve su región, equipo operativo ve procesos)
   - **Aprendizaje:** Diferentes usuarios necesitan diferentes vistas; un dashboard debe asumir una audiencia clara

4. **Interpretar la alta tasa de cancelación (33%):**
   - **Problema:** Sorprendente; ¿es problema real o artifact de datos?
   - **Solución:** Validé el dato en el índice de Elasticsearch (conteo manual), confirma que es real
   - **Aprendizaje:** Cuando un patrón sorprende, validar la fuente antes de sacar conclusiones

5. **Reconocer limitaciones del análisis:**
   - **Problema:** Fácil caer en "los datos dicen X" sin considerar context faltante
   - **Solución:** Deliberadamente documenté 5+ limitaciones del dashboard
   - **Aprendizaje:** Un análisis honesto reconoce qué no sabe. Kibana es poderoso pero no responde todo

**Resoluciones generales:**
- Mantuve mentalidad crítica: cuestionar cada decisión de diseño
- Iteré: primer draft fue diferente al final, mejorando con reflexión
- Documenté: escribir el análisis me obligó a ser preciso sobre lo que afirmo

---

## 12. Conclusión

Resume en 2–3 líneas qué ha supuesto este laboratorio dentro de la UD3 y cómo conecta con los laboratorios anteriores.

---

El Laboratorio 3 **cierra el ciclo completo de la UD3** actuando como síntesis de todos los aprendizajes: mientras el Lab 1 enseñó exploración básica, el Lab 2 enseñó análisis comparativo, el Lab 3 enseña **pensamiento crítico sobre datos integrados**. Este laboratorio demuestra que en sistemas Big Data reales, la visualización es solo la punta del iceberg; el verdadero valor está en la capacidad de un equipo de **interpretar, cuestionar y actuar sobre insights** extraídos de dashboards bien diseñados. Los Labs 1-3 de Kibana complementan el pipeline Big Data iniciado en Labs anteriores (ingesta con Flume/Kafka, procesamiento con Spark, limpieza en Zeppelin) proporcionando la **capa final de inteligencia** donde los datos procesados se transforman en decisiones de negocio medibles.

---

## Fin del documento de entrega

