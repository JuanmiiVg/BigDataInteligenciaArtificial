# UD3 — Laboratorio 2 de Kibana  
## Documento de entrega

---

### Módulo
Sistemas de Big Data

### Unidad Didáctica
UD3 — Procesamiento y visualización de datos en sistemas Big Data

### Laboratorio
Laboratorio 2 — Dashboards y análisis con Kibana

---

## 1. Datos del grupo

**Alumno/a(s):**

- Nombre y apellidos: Juan Manuel Vega Carrillo
- Nombre y apellidos (si procede):

**Grupo:** Big Data  
**Fecha de entrega:** 26 de enero de 2026

---

## 2. Contexto del laboratorio

En este laboratorio se ha profundizado en el uso de **Kibana** como herramienta de análisis y visualización de datos, centrándose en el **diseño de dashboards útiles** y en la **interpretación de la información mostrada**.

Se parte de datos ya procesados y almacenados en **Elasticsearch**, sin modificar su estructura.

---

## 3. Datos analizados

Indica brevemente:

- **Índice(s) utilizados en Elasticsearch:** ventas
- **Tipo de datos:** Ventas de productos tecnológicos (laptops, smartphones, tablets, monitores, teclados, ratones, auriculares) con información de ciudades españolas, categorías, cantidades, precios, estados de pedido y vendedores
- **Campo temporal utilizado:** fecha (rango de 90 días desde la fecha actual hacia atrás)

**Estructura de datos:** El índice contiene 500 registros de ventas con campos como ciudad (Madrid, Barcelona, Valencia, Sevilla, Bilbao), producto, categoría (Electrónica, Informática, Accesorios), cantidad, precio unitario, total, estado (Completado, Pendiente, Cancelado) y vendedor.

---

## 4. Exploración avanzada con Discover

Describe el trabajo realizado en **Discover**:

**Filtros combinados aplicados:**

1. **Filtro por ciudad:** ciudad = "Madrid" - Para analizar el rendimiento específico de la capital
2. **Filtro por estado:** estado = "Completado" - Para enfocarnos solo en ventas finalizadas exitosamente
3. **Combinación adicional probada:** ciudad = "Barcelona" AND categoria = "Electrónica" - Para análisis segmentado por ubicación y tipo de producto

La aplicación de filtros combinados redujo el dataset de 500 documentos a aproximadamente 25-35 registros, permitiendo un análisis más específico y detallado de ese segmento.

**Cambios de rango temporal realizados:**

- **Last 7 days:** Mostró datos recientes con aproximadamente 35-40 documentos, útil para análisis de tendencias inmediatas
- **Last 30 days:** Rango medio con ~170 documentos, equilibrio entre detalle y panorama general
- **Last 90 days:** Rango completo con los 500 documentos, necesario para análisis de patrones y tendencias estacionales

El cambio de rangos temporales permitió identificar que las ventas se distribuyen de forma relativamente uniforme en el tiempo, sin picos extremos evidentes.

**Patrones, valores dominantes o anomalías detectadas:**

- **Distribución equilibrada por ciudades:** No hay una ciudad claramente dominante, las ventas están distribuidas de forma bastante homogénea entre las 5 ciudades
- **Categoría Electrónica dominante en valor:** Los productos de Electrónica (Laptop, Smartphone, Tablet) generan mayor valor total debido a sus precios más elevados
- **Tasa de cancelación significativa:** Aproximadamente un 30-35% de los pedidos están en estado "Cancelado", lo que podría indicar problemas en el proceso de compra o disponibilidad
- **Productos más frecuentes:** Los accesorios (ratones, teclados, auriculares) aparecen con mayor frecuencia pero menor valor individual
- **Vendedores activos:** Algunos vendedores (Vendedor_3, Vendedor_7, Vendedor_12) aparecen con mayor frecuencia en los registros
- **Precios variables:** Rango amplio de precios desde 10€ (accesorios) hasta 1500€ (laptops de gama alta)

**CAPTURA 1: Exploración en Discover con filtros combinados aplicados**
![CAPTURA 1 - Discover con filtros](Captura/captura1.png)

---

## 5. Visualizaciones comparativas

Describe al menos **dos visualizaciones comparativas** creadas durante el laboratorio.

### 5.1 Visualización Comparativa 1: Ventas por Categoría de Producto

- **Tipo de visualización:** Gráfico de barras verticales
- **Qué campos utiliza:** 
  - Eje X (horizontal): `categoria` (Electrónica, Informática, Accesorios)
  - Eje Y (vertical): `total` con agregación Sum (suma de ingresos totales)
- **Qué comparación permite realizar:** Permite comparar directamente los ingresos totales generados por cada categoría de productos, identificando cuál es la más rentable
- **Qué información relevante aporta:** 
  - **Electrónica** genera los mayores ingresos totales debido al alto precio unitario de laptops, smartphones y tablets
  - **Informática** tiene un rendimiento intermedio con monitores, teclados y ratones
  - **Accesorios** genera menores ingresos a pesar de venderse en mayores cantidades
  - Esta información es crucial para decisiones de inventario, marketing y asignación de recursos comerciales

**CAPTURA 2: Comparativa de Ventas por Categoría**
![CAPTURA 2 - Ventas por Categoría](Captura/captura2.png)

---

### 5.2 Visualización Comparativa 2: Evolución Temporal de Ventas

- **Tipo de visualización:** Gráfico de líneas temporales (Line chart)
- **Qué campos utiliza:**
  - Eje X (horizontal): `fecha` con intervalo automático (diario/semanal)
  - Eje Y (vertical): `total` con agregación Sum
  - Break down (opcional): `ciudad` para mostrar múltiples líneas
- **Qué comparación permite realizar:** Permite comparar la evolución temporal de las ventas, identificar tendencias ascendentes/descendentes, picos de actividad y comparar el rendimiento entre diferentes ciudades a lo largo del tiempo
- **Qué información relevante aporta:**
  - Identifica **períodos de mayor actividad** comercial
  - Muestra si hay **tendencias estacionales** o patrones recurrentes
  - Permite detectar **anomalías** o caídas inesperadas en ventas
  - Si se segmenta por ciudad, revela qué ubicaciones tienen mejor evolución temporal
  - Útil para planificación de campañas y previsión de demanda

**CAPTURA 3: Evolución Temporal de Ventas**
![CAPTURA 3 - Evolución Temporal](Captura/captura3.png)

---

### 5.3 Visualización Comparativa 3: Distribución por Estado de Pedido

- **Tipo de visualización:** Gráfico Donut (o Pie chart)
- **Qué campos utiliza:**
  - Slice by: `estado` (Completado, Pendiente, Cancelado)
  - Métrica: Count of records (conteo de documentos)
- **Qué comparación permite realizar:** Permite comparar la proporción de pedidos según su estado final, visualizando de forma clara qué porcentaje de pedidos se completan exitosamente frente a los que quedan pendientes o se cancelan
- **Qué información relevante aporta:**
  - **Tasa de éxito** del proceso de venta (% de completados)
  - **Tasa de cancelación** que puede indicar problemas operativos
  - **Pedidos pendientes** que requieren seguimiento
  - Esta información es crítica para optimizar el proceso de ventas y reducir pérdidas
  - Ayuda a identificar cuellos de botella en el proceso de compra

**CAPTURA 4: Distribución por Estado de Pedido**
![CAPTURA 4 - Distribución Estados](Captura/captura4.png)

---

## 6. Dashboard con filtros

Describe el dashboard creado:

**Visualizaciones incluidas:**

1. **Total Ventas (Métrica):** KPI principal mostrando la suma total de ingresos, posicionado en la parte superior como referencia rápida
2. **Ventas por Ciudad (Barras verticales):** Comparativa de ingresos por ubicación geográfica
3. **Comparativa por Categoría (Barras verticales):** Análisis de rendimiento por tipo de producto
4. **Evolución Temporal (Líneas):** Tendencia de ventas a lo largo del tiempo
5. **Distribución por Estado (Donut):** Proporción de pedidos según su estado final
6. **Productos más vendidos (Barras horizontales):** Ranking de productos por cantidad de unidades vendidas

**Diseño del dashboard:** Las visualizaciones están organizadas jerárquicamente con la métrica principal en la parte superior, seguida de gráficos comparativos en el centro y análisis temporal en la parte inferior. El diseño facilita la lectura de arriba hacia abajo, del dato agregado al detalle.

---

**Filtros utilizados (tipo, categoría, ciudad, etc.):**

1. **Control de filtro por Ciudad:** 
   - Tipo: Options list control
   - Campo: `ciudad`
   - Valores: Madrid, Barcelona, Valencia, Sevilla, Bilbao
   - Permite selección múltiple

2. **Control de filtro por Categoría:**
   - Tipo: Options list control
   - Campo: `categoria`
   - Valores: Electrónica, Informática, Accesorios
   - Permite selección múltiple

3. **Filtro temporal (Time picker):**
   - Rango seleccionable desde la barra superior de Kibana
   - Permite ajustar el período de análisis dinámicamente

**Ubicación de controles:** Los filtros están posicionados en la parte superior del dashboard, justo debajo de la barra de título, para fácil acceso y visibilidad.

---

**Cómo afectan los filtros a las visualizaciones:**

**Comportamiento dinámico:**
- Al **seleccionar "Barcelona" en el filtro de ciudad**, todas las visualizaciones se actualizan instantáneamente:
  - La métrica de Total Ventas muestra solo los ingresos de Barcelona
  - El gráfico de Ventas por Ciudad resalta Barcelona y oculta/atenúa las demás
  - La Evolución Temporal muestra solo la línea de Barcelona
  - Todas las agregaciones se recalculan para ese subconjunto

- Al **combinar filtros** (ej: Barcelona + Electrónica):
  - El dataset se reduce a la intersección de ambos criterios
  - La métrica muestra el total de ventas de productos electrónicos en Barcelona
  - Los gráficos muestran solo productos de la categoría Electrónica vendidos en Barcelona
  - Permite análisis muy específico y segmentado

**Ventajas de los filtros interactivos:**
- **Sin necesidad de crear múltiples dashboards** para diferentes segmentaciones
- **Exploración ad-hoc** permitiendo al usuario hacer preguntas dinámicas
- **Respuesta inmediata** sin necesidad de recargar o regenerar visualizaciones
- **Democratización del análisis** - usuarios no técnicos pueden explorar datos por sí mismos

**Ejemplo de uso práctico:**
Un responsable comercial puede filtrar por su ciudad (Madrid) para ver su rendimiento específico, luego añadir el filtro de "Electrónica" para analizar esa categoría en particular, y finalmente ajustar el rango temporal a "Last 30 days" para ver tendencias recientes. Todo esto sin necesidad de soporte técnico o consultas SQL.

**CAPTURA 5: Dashboard completo con filtros aplicados**
![CAPTURA 5 - Dashboard con Filtros](Captura/captura5.png)

*Nota: La captura debe mostrar los controles de filtro en la parte superior con al menos un filtro seleccionado (ej: Barcelona + Electrónica) y las visualizaciones actualizadas reflejando esa selección.*

---

## 7. Análisis e interpretación de resultados

Responde a las siguientes cuestiones:

### 1. ¿Qué información relevante se obtiene del dashboard?

El dashboard proporciona información **accionable** en múltiples dimensiones:

**Información financiera:**
- **Ingresos totales** en el período analizado (KPI principal)
- **Distribución geográfica de ingresos** - qué ciudades generan más valor
- **Rentabilidad por categoría** - qué tipo de productos son más lucrativos

**Información operativa:**
- **Tasa de éxito/fracaso** de pedidos (distribución por estado)
- **Volumen de ventas canceladas** que representa pérdida de ingresos potenciales
- **Tendencias temporales** que permiten identificar períodos de alta/baja actividad

**Información comercial:**
- **Productos más demandados** por volumen de unidades
- **Equilibrio entre ciudades** - si hay mercados saturados o desatendidos
- **Comparativa de categorías** para priorización de inventario

**Valor estratégico:**
Esta información permite a diferentes stakeholders tomar decisiones: directores sobre estrategia comercial, responsables de compras sobre inventario, equipos de marketing sobre segmentación geográfica, y gestores operativos sobre procesos de venta.

---

### 2. ¿Qué patrones o tendencias se observan?

**Patrones identificados:**

1. **Distribución geográfica equilibrada:** Las cinco ciudades (Madrid, Barcelona, Valencia, Sevilla, Bilbao) muestran rendimientos similares sin dominancia clara de una sobre otras. Esto sugiere:
   - Penetración de mercado homogénea
   - Estrategia comercial equilibrada
   - Oportunidad de crecimiento uniforme

2. **Disparidad valor vs volumen:** 
   - Electrónica genera **mayores ingresos** con **menor volumen** de ventas
   - Accesorios tienen **mayor volumen** pero **menor valor** total
   - Informática se posiciona en el término medio
   - Patrón típico de retail tecnológico

3. **Tasa de cancelación significativa (~33%):**
   - Un tercio de los pedidos no se completan
   - Patrón consistente que sugiere problemas sistemáticos, no aleatorios
   - Puede indicar problemas de disponibilidad, precios, o proceso de checkout

4. **Tendencia temporal estable:**
   - No se observan picos extremos o valles pronunciados
   - Ventas distribuidas uniformemente en el tiempo
   - Ausencia de estacionalidad marcada en el período de 90 días
   - Podría indicar demanda constante o falta de estacionalidad en el sector

5. **Sin outliers evidentes:**
   - No hay vendedores, productos o días con rendimiento extremadamente atípico
   - Comportamiento predecible y modelizable

---

### 3. ¿Qué información consideras que falta para mejorar el análisis?

**Información financiera adicional:**
- **Costos de adquisición de productos** - actualmente solo vemos precio de venta
- **Margen de beneficio** por producto/categoría - clave para decisiones estratégicas
- **Costos operativos** (logística, personal) para calcular rentabilidad neta
- **Descuentos aplicados** - si existen promociones que afecten márgenes

**Información de clientes:**
- **Segmentación demográfica** (edad, género, perfil profesional)
- **Clientes nuevos vs recurrentes** - análisis de retención
- **Valor de vida del cliente (CLV)**
- **Tasa de conversión** desde visita hasta compra
- **Origen del cliente** (web, tienda física, móvil)

**Información operativa:**
- **Motivo de cancelaciones** - ¿por qué se cancelan los pedidos?
- **Tiempo de procesamiento** de pedidos
- **Disponibilidad de stock** al momento de la venta
- **Método de pago** utilizado y su relación con cancelaciones
- **Datos de logística** (tiempos de entrega, costos de envío)

**Información de contexto:**
- **Datos de competencia** - participación de mercado
- **Eventos externos** (campañas, festivos, eventos locales) que expliquen picos
- **Datos macroeconómicos** que puedan correlacionar con ventas
- **Feedback de clientes** y valoraciones de productos

**Métricas calculadas:**
- **Ticket medio** por transacción
- **Productos por pedido** (cross-selling)
- **Tasa de conversión por canal**
- **ROI de campañas** de marketing

---

### 4. ¿Qué errores de interpretación podrían cometerse al analizar estos gráficos?

**Errores comunes de interpretación:**

1. **Confundir ingresos con beneficio:**
   - El total de ventas muestra **ingresos brutos**, no beneficio neto
   - Sin datos de costos, no sabemos si Electrónica es realmente más rentable
   - Una categoría con mayor ingreso podría tener menor margen

2. **Ignorar el contexto temporal:**
   - Comparar ciudades sin considerar que pueden tener diferentes períodos de actividad
   - No considerar eventos locales (festivos, campañas) que afectan ventas
   - Asumir que 90 días son representativos de todo el año (estacionalidad)

3. **Correlación vs causalidad:**
   - Ver que Barcelona vende más Electrónica no significa que sea por características de la ciudad
   - Podría ser por ubicación de tiendas, campañas específicas, o simple azar en 90 días

4. **Sesgo de selección con filtros:**
   - Al filtrar solo "Completado", perdemos información sobre productos con mayor tasa de cancelación
   - Análisis sesgado que no muestra problemas reales

5. **Ignorar productos cancelados:**
   - 33% de cancelaciones representa **ingresos potenciales perdidos**
   - No incluir esto en planificación puede llevar a subestimar capacidad real

6. **Comparar categorías sin normalizar:**
   - Electrónica tiene productos más caros, obvio que genera más ingresos
   - Debería compararse por **margen unitario** o **rentabilidad relativa**

7. **Asumir tendencias lineales:**
   - Una tendencia de 90 días no garantiza comportamiento futuro
   - Extrapolación sin considerar eventos futuros puede ser peligrosa

8. **Ignorar segmentos pequeños:**
   - Enfocarse solo en lo más vendido puede hacer perder oportunidades en nichos
   - Productos de baja rotación podrían tener mayor margen

9. **Promedios engañosos:**
   - El "promedio" de ventas por ciudad oculta la variabilidad interna
   - Una ciudad puede tener días excelentes y días pésimos con promedio normal

10. **Falta de benchmarking:**
    - Sin comparativa con períodos anteriores o competencia, no sabemos si los números son buenos o malos
    - Un millón en ventas puede ser excelente o desastroso según el contexto

**Recomendaciones para evitar errores:**
- Siempre incluir **contexto temporal y referencias**
- Documentar **suposiciones y limitaciones** del análisis
- Complementar dashboards con **análisis cualitativo**
- Validar hallazgos con **fuentes adicionales de datos**
- Mantener escepticismo saludable ante **patrones aparentes**

---

## 8. Comparación con otras herramientas

Reflexiona brevemente:

### 1. ¿Qué tipo de análisis realizarías mejor con Spark o Python?

**Análisis ideales para Spark:**

- **Procesamiento masivo de datos:** Cuando el volumen supera la capacidad de visualización (millones/miles de millones de registros)
- **Transformaciones complejas ETL:** Limpieza, normalización, enriquecimiento de datos antes de la visualización
- **Machine Learning:** Modelos predictivos, clustering, clasificación, detección de anomalías con algoritmos complejos
- **Agregaciones multicapa:** Cálculos que requieren múltiples pasos de agregación y transformación
- **Procesamiento batch:** Análisis históricos completos que no requieren interactividad inmediata
- **Joins complejos:** Combinación de múltiples fuentes de datos heterogéneas
- **Procesamiento distribuido:** Cuando se requiere paralelización para tiempos razonables de ejecución

**Ejemplo:** Calcular el valor de vida del cliente (CLV) analizando 5 años de transacciones de 10 millones de clientes, requiriendo joins entre tablas de ventas, devoluciones, costos y segmentación.

**Análisis ideales para Python (pandas, scikit-learn, etc.):**

- **Análisis estadístico avanzado:** Regresiones, test de hipótesis, análisis de varianza (ANOVA)
- **Visualizaciones personalizadas:** Gráficos complejos no disponibles en Kibana (networks, heatmaps complejos, 3D)
- **Modelos predictivos ligeros:** Cuando los datos caben en memoria y se necesita experimentación rápida
- **Análisis exploratorio inicial:** Notebook-style para investigación y prototipado
- **Automatización de reportes:** Scripts programados para generar informes periódicos en PDF/HTML
- **Integración con APIs:** Cuando se necesita combinar datos de múltiples APIs externas
- **Análisis científico específico:** Series temporales complejas, análisis de señales, procesamiento de imágenes

**Ejemplo:** Crear un modelo de regresión logística para predecir la probabilidad de cancelación de pedido basado en 15 variables, con validación cruzada y análisis de feature importance.

**Cuándo usar cada uno:**
- **Spark:** Volumen masivo, procesamiento distribuido necesario
- **Python:** Análisis profundo con datasets medianos, prototipado, personalización extrema
- **Kibana:** Visualización interactiva de resultados, exploración ad-hoc, monitoreo en tiempo real

---

### 2. ¿Qué tipo de análisis encaja mejor con Kibana?

**Fortalezas de Kibana:**

**1. Exploración interactiva en tiempo real:**
- Usuarios no técnicos pueden **hacer preguntas sobre los datos dinámicamente**
- Cambios de filtros, rangos temporales, segmentaciones al instante
- No requiere reejecutar código o consultas
- **Ejemplo:** "¿Cómo fueron las ventas de Electrónica en Madrid la semana pasada?"

**2. Monitoreo operacional:**
- Dashboards actualizados automáticamente con nuevos datos
- Detección de anomalías visuales en tiempo real
- Ideal para **métricas de negocio que cambian constantemente** (ventas diarias, tráfico web, logs de aplicación)
- **Ejemplo:** Dashboard de operaciones mostrando ventas del día actual, actualizándose cada minuto

**3. Análisis de logs y eventos:**
- Diseñado nativamente para logs timestamped
- Búsqueda full-text en campos de texto
- Correlación temporal de eventos
- **Ejemplo:** Analizar logs de aplicación para identificar errores correlacionados con caídas de ventas

**4. Democratización del análisis:**
- **Cualquier usuario** (marketing, ventas, operaciones) puede explorar datos
- No requiere conocimientos de SQL, Python o programación
- Autoservicio analítico sin dependencia del equipo técnico
- **Ejemplo:** Responsable comercial explorando rendimiento de su región sin ayuda de IT

**5. Dashboards ejecutivos:**
- KPIs visuales de alto nivel para dirección
- Drill-down para profundizar en detalles sin cambiar de herramienta
- Compartir mediante URL sin exportar imágenes
- **Ejemplo:** Dashboard ejecutivo con métricas clave del negocio visible en pantallas de oficina

**6. Análisis comparativo simple:**
- Comparaciones entre categorías, regiones, períodos
- Distribuciones y proporciones
- Tendencias temporales
- **Ejemplo:** "¿Qué ciudad vende más? ¿Qué producto es más popular?"

**Limitaciones de Kibana:**
- No es ideal para análisis estadístico profundo (regresiones, ANOVA)
- Limitado para machine learning
- Las agregaciones muy complejas son difíciles de configurar
- No hay scripting o automatización avanzada

---

### 3. ¿Qué ventajas aporta Kibana frente a herramientas de BI clásicas?

**Ventajas principales:**

**1. Velocidad y rendimiento con Big Data:**
- **Optimizado para Elasticsearch:** Consultas sobre millones de registros en milisegundos
- **Índices invertidos:** Búsquedas full-text extremadamente rápidas
- **Agregaciones eficientes:** Cálculos en tiempo real incluso con datasets masivos
- **BI clásico:** Puede requerir cubos OLAP precalculados, más lento en consultas ad-hoc

**2. Análisis en tiempo real:**
- **Kibana:** Datos disponibles para visualización en **segundos** tras su ingesta
- **BI clásico:** Típicamente requiere **procesos ETL batch** (nocturnos o cada hora)
- **Ejemplo:** Dashboard de ventas mostrando transacciones de hace 5 segundos vs reportes del día anterior

**3. Integración nativa con Elastic Stack:**
- **Pipeline completo:** Beats → Logstash → Elasticsearch → Kibana
- **Sin necesidad de conectores** o adaptadores entre componentes
- **Stack unificado:** Logs, métricas, APM, seguridad, todo en la misma plataforma
- **BI clásico:** Requiere conectores para cada fuente, más puntos de fallo

**4. Enfoque en logs y eventos:**
- **Diseñado para datos timestamped** con alta cardinalidad
- **Búsqueda full-text** nativa en todos los campos
- **Pattern detection** en logs
- **BI clásico:** Optimizado para datos estructurados relacionales, menos eficiente con logs

**5. Menor costo de infraestructura:**
- **Open source** (versión básica gratuita)
- **Sin licencias por usuario** (en versión OSS)
- **Despliegue flexible:** On-premise, cloud, híbrido
- **BI clásico:** Tableau, Power BI, Qlik tienen costos por usuario/despliegue significativos

**6. Curva de aprendizaje:**
- **Interfaz intuitiva:** Lens hace visualizaciones con drag-and-drop
- **Menos conceptos complejos:** No requiere entender cubos, dimensiones, medidas OLAP
- **BI clásico:** Puede requerir certificaciones, curvas de aprendizaje pronunciadas

**7. DevOps y observabilidad:**
- **Cultura DevOps:** Kibana es estándar en observabilidad y monitoreo
- **Logs, métricas, traces** en una sola herramienta
- **Alerting integrado:** Detección de anomalías y alertas
- **BI clásico:** Enfocado en análisis de negocio, no operacional

**8. Flexibilidad y extensibilidad:**
- **API REST completa:** Automatización mediante scripts
- **Visualizaciones custom:** Desarrollo de plugins propios
- **Integración con Jupyter:** Notebooks para análisis avanzado
- **BI clásico:** Ecosistemas más cerrados, menos extensibles

**Desventajas de Kibana vs BI clásico:**

- **Modelado de datos:** BI clásico tiene mejores capacidades de modelado dimensional
- **Análisis predictivo:** Power BI, Tableau tienen integraciones más maduras con ML
- **Visualizaciones avanzadas:** BI clásico ofrece más tipos de gráficos out-of-the-box
- **Governance empresarial:** Herramientas BI tienen mejor control de accesos, certificación de datos
- **Soporte y formación:** Vendors como Microsoft, Tableau ofrecen soporte empresarial más robusto

**Cuándo elegir cada uno:**

| Escenario | Kibana | BI Clásico |
|-----------|--------|------------|
| Análisis de logs y eventos | ✅ Excelente | ❌ Limitado |
| Tiempo real crítico | ✅ Excelente | ⚠️ Limitado |
| Volúmenes masivos (TB+) | ✅ Muy bueno | ⚠️ Requiere optimización |
| Usuarios no técnicos | ✅ Bueno | ✅ Excelente |
| Análisis de negocio tradicional | ⚠️ Adecuado | ✅ Excelente |
| Modelado dimensional complejo | ❌ Limitado | ✅ Excelente |
| Presupuesto limitado | ✅ Open source | ⚠️ Licencias caras |
| DevOps/Observabilidad | ✅ Estándar | ❌ No aplicable |

**Conclusión:** Kibana destaca en escenarios **Big Data, tiempo real, logs y observabilidad** con costos reducidos. BI clásico es superior en **análisis de negocio estructurado, modelado dimensional y visualizaciones avanzadas** con presupuesto disponible. En entornos modernos, **ambas herramientas coexisten**: Kibana para operaciones y monitoreo, BI para reportes ejecutivos y análisis de negocio.

---

## 9. Reflexión final

Reflexiona brevemente sobre:

- Qué aporta Kibana dentro de un sistema Big Data.
- La importancia del diseño de dashboards.
- La diferencia entre visualizar datos y analizarlos.

(Extensión orientativa: 5–10 líneas)

---

Este laboratorio ha profundizado mi comprensión de que **Kibana no es solo una herramienta de gráficos, sino una capa crítica de inteligencia de negocio** dentro de una arquitectura Big Data. Mientras que herramientas como Spark procesan y transforman datos, Kibana **democratiza el acceso a insights**, permitiendo que usuarios sin conocimientos técnicos puedan tomar decisiones basadas en datos. He aprendido que un dashboard bien diseñado **no es una colección de gráficos bonitos**, sino una **narrativa visual** que responde preguntas específicas de negocio con la mínima carga cognitiva posible.

La **diferencia fundamental entre visualizar y analizar** quedó clara en este laboratorio: visualizar es simplemente representar datos gráficamente, mientras que analizar implica **interpretar, cuestionar, contextualizar y extraer conclusiones accionables**. Un gráfico de barras puede mostrar que Barcelona vende más, pero el análisis profundo pregunta: ¿por qué?, ¿es sostenible?, ¿qué factores externos influyen?, ¿qué podemos aprender para otras ciudades? Esta distinción es crucial en entornos Big Data donde el volumen de datos puede abrumar; la visualización ayuda a **reducir la complejidad**, pero el análisis crítico es lo que genera **valor real** para la organización.

La importancia del **diseño intencional de dashboards** no puede subestimarse: cada visualización debe tener un propósito claro, cada filtro debe facilitar una exploración específica, y el layout debe guiar al usuario naturalmente desde los KPIs globales hacia los detalles. Un dashboard mal diseñado puede llevar a decisiones erróneas por mala interpretación, mientras que uno bien pensado se convierte en una **herramienta estratégica de negocio**. En proyectos Big Data reales, donde los stakeholders tienen diferentes niveles técnicos y necesidades distintas, Kibana actúa como el **puente entre datos complejos y decisiones simples**, cerrando el ciclo de valor del dato: desde la captura hasta la acción informada.

---

## 10. Dificultades encontradas (opcional)

Indica si has tenido problemas técnicos o conceptuales y cómo los has resuelto.

**Dificultades técnicas:**

1. **Configuración de controles de filtro en dashboard:**
   - **Problema:** Inicialmente no encontraba cómo añadir controles interactivos (options list) al dashboard
   - **Solución:** Descubrí que en Kibana 8.x hay que usar el botón "Add panel" y buscar "Controls" en lugar de estar en un menú separado como en versiones anteriores
   - **Aprendizaje:** La interfaz de Kibana ha evolucionado y es importante consultar documentación de la versión específica

2. **Agregaciones en gráfico temporal:**
   - **Problema:** El gráfico de línea temporal mostraba demasiados puntos y se veía saturado
   - **Solución:** Ajusté el intervalo de agregación en el eje temporal de "Auto" a "Daily" o "Weekly" según el rango seleccionado
   - **Aprendizaje:** Kibana permite controlar la granularidad temporal para equilibrar detalle vs legibilidad

3. **Break down por múltiples campos:**
   - **Problema:** Quise hacer un breakdown por ciudad Y categoría simultáneamente en una visualización
   - **Solución:** Me di cuenta de que esto complica excesivamente el gráfico; mejor crear visualizaciones separadas o usar filtros globales
   - **Aprendizaje:** Más capas de datos no siempre significan mejor análisis; la simplicidad es clave

**Dificultades conceptuales:**

1. **Diferencia entre filtros de visualización y filtros de dashboard:**
   - **Problema:** No entendía por qué algunos filtros afectaban todas las visualizaciones y otros solo una
   - **Solución:** Comprendí que los filtros aplicados a nivel de dashboard son globales, mientras que los aplicados en una visualización específica son locales
   - **Aprendizaje:** La jerarquía de filtros es importante para diseñar interacciones correctas

2. **Elección del tipo de visualización apropiado:**
   - **Problema:** Dudaba entre usar gráfico de barras, líneas o área para mostrar evolución temporal
   - **Solución:** Experimenté con los tres tipos y concluí que líneas son mejores para tendencias continuas, barras para comparaciones discretas
   - **Aprendizaje:** El tipo de visualización debe elegirse según la historia que se quiere contar, no por estética

3. **Interpretación de agregaciones:**
   - **Problema:** Confundía "Count" con "Sum of cantidad" en el contexto de ventas
   - **Solución:** Analicé ejemplos concretos: Count cuenta documentos (pedidos), Sum of cantidad suma unidades vendidas, Sum of total suma ingresos
   - **Aprendizaje:** Cada agregación responde una pregunta diferente; es crucial elegir la correcta según lo que se quiere medir

4. **Contexto necesario para interpretación:**
   - **Problema:** Al ver que una ciudad tenía más ventas, inicialmente asumí que era por mejor rendimiento comercial
   - **Solución:** Reflexioné que podría ser por mayor población, más tiendas, campañas específicas, o incluso azar en 90 días
   - **Aprendizaje:** Los datos sin contexto pueden llevar a conclusiones erróneas; siempre hay que cuestionar los hallazgos aparentes

**Resoluciones generales:**
- **Documentación oficial de Elastic:** Consulté la documentación de Kibana 8.x para funcionalidades específicas
- **Experimentación iterativa:** Probé diferentes configuraciones y observé el resultado en lugar de buscar la "configuración perfecta" desde el inicio
- **Pensamiento crítico:** Cuestioné cada visualización preguntándome "¿qué decisión permite tomar esto?" antes de incluirla en el dashboard
- **Comparación con Lab 1:** Reutilicé conocimientos del laboratorio anterior sobre Data Views, Discover y visualizaciones básicas

---

## 11. Conclusión

Resume en 2–3 líneas qué has aprendido en este laboratorio y cómo encaja con lo trabajado anteriormente en la UD3.

---

En este laboratorio he evolucionado desde crear visualizaciones simples (Lab 1) hacia **diseñar dashboards analíticos con propósito estratégico**, comprendiendo que la verdadera potencia de Kibana reside en los **filtros interactivos y la exploración dinámica** que permiten a usuarios de negocio responder preguntas ad-hoc sin dependencia técnica. He aprendido que un dashboard efectivo no solo muestra datos, sino que **guía la toma de decisiones** mediante una narrativa visual clara, filtros bien diseñados y visualizaciones que se complementan entre sí. Este laboratorio cierra el ciclo de la UD3 iniciado con procesamiento en Spark (Lab p3) y análisis interactivo en Zeppelin, posicionando a Kibana como la **capa de democratización** que hace accesibles los insights de Big Data a toda la organización, transformando datos procesados en información accionable para stakeholders no técnicos.

---

## Fin del documento de entrega