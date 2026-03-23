# UD3 — Laboratorio 2  
## Visualización de datos con Kibana  
### Documento de entrega

---

### Módulo
Sistemas de Big Data

### Unidad Didáctica
UD3 — Procesamiento y visualización de datos en sistemas Big Data

### Laboratorio
Laboratorio 2 — Creación de visualizaciones con Kibana

---

## 1. Datos del grupo

**Alumno/a(s):**
- Nombre y apellidos: Juan Manuel Vega Carrillo
- Nombre y apellidos (si procede): 

**Grupo:** Big Data  
**Fecha de entrega:** 26 de enero de 2026

---

## 2. Objetivo del laboratorio

El objetivo de este laboratorio ha sido **crear visualizaciones significativas en Kibana** a partir de un conjunto de datos ya explorado, utilizando la **Visualize Library**, y comprendiendo el papel de las visualizaciones dentro de un flujo de análisis Big Data.

---

## 3. Entorno de trabajo

Describe brevemente el entorno utilizado:

- Versión de Elasticsearch: 8.11.3
- Versión de Kibana: 8.11.3
- Forma de despliegue (Docker, local, etc.): Docker Compose

**CAPTURA 1: Data View creado en Stack Management**
![CAPTURA 1 - Data View](Captura/captura1.png)

---

## 4. Data View utilizado

Indica la información del **Data View** empleado:

- Nombre del Data View: Ventas
- Patrón de índices: ventas*
- Campo temporal seleccionado (si procede): fecha

El Data View permite a Kibana acceder al índice `ventas` que contiene 500 registros de ventas generadas con datos de ciudades españolas, productos tecnológicos, cantidades, precios y estados de pedido durante los últimos 90 días.

---

## 5. Visualizaciones creadas

Indica las visualizaciones que has creado (al menos tres):

### 5.1 Visualización 1: Ventas por Ciudad

- Tipo de visualización (barras, líneas, etc.): Gráfico de barras verticales
- Métrica principal: Suma del total de ventas (Sum of total)
- Campo(s) de agrupación: ciudad
- Información que aporta: Permite identificar qué ciudad genera más ingresos totales, facilitando la toma de decisiones sobre distribución de recursos, campañas de marketing o apertura de nuevos puntos de venta. Se puede observar la comparativa directa entre Madrid, Barcelona, Valencia, Sevilla y Bilbao.

**CAPTURA 2: Discover con filtros aplicados**
![CAPTURA 2 - Discover con filtros](Captura/captura2.png)

**CAPTURA 3: Visualización de Ventas por Ciudad**
![CAPTURA 3 - Ventas por Ciudad](Captura/captura3.png)

---

### 5.2 Visualización 2: Productos más vendidos

- Tipo de visualización: Gráfico de barras horizontales
- Métrica principal: Suma de cantidades vendidas (Sum of cantidad)
- Campo(s) de agrupación: producto
- Información que aporta: Muestra qué productos tienen mayor demanda en términos de unidades vendidas. Esta información es crucial para gestión de inventario, planificación de compras y detección de productos estrella. Permite identificar si hay productos con baja rotación que podrían requerir estrategias comerciales diferentes.

**CAPTURA 4: Visualización de Productos más vendidos**
![CAPTURA 4 - Productos más vendidos](Captura/captura4.png)

---

### 5.3 Visualización 3: Total de Ventas

- Tipo de visualización: Métrica (Metric)
- Métrica principal: Suma total de ingresos (Sum of total)
- Campo(s) de agrupación: Sin agrupación (métrica global)
- Información que aporta: Proporciona un KPI (Key Performance Indicator) del total de ingresos generados en el período analizado. Es un indicador clave para dirección y gestión, permitiendo visualizar de forma inmediata el rendimiento global del negocio. Ideal para dashboards ejecutivos.

**CAPTURA 5: Visualización de Total Ventas (Métrica)**
![CAPTURA 5 - Total Ventas](Captura/captura5.png)

---

## 6. Coherencia con la exploración inicial

Responde de forma razonada:

1. **¿Coinciden las visualizaciones con lo observado en Discover en el Laboratorio 1?**
   
   Sí, las visualizaciones coinciden perfectamente con lo observado en Discover. Al explorar los datos inicialmente en Discover, ya se podía ver mediante los conteos de campos que ciertas ciudades y productos aparecían con mayor frecuencia. Las visualizaciones creadas simplemente agregan y presentan estos datos de forma más clara y visual, facilitando la comparación.

2. **¿Ha habido alguna visualización cuyo resultado no esperabas?**
   
   Al principio me sorprendió la distribución relativamente equilibrada de ventas entre ciudades, esperaba que Madrid o Barcelona dominaran de forma más clara. También fue interesante observar que los productos de menor precio (como ratones y teclados) no necesariamente son los más vendidos en cantidad, lo que sugiere que los clientes también compran productos de mayor valor.

3. **¿Has tenido que modificar algún filtro o rango temporal para que la visualización fuese útil?**
   
   Sí, inicialmente el rango temporal estaba en "Last 15 minutes" por defecto. Tuve que ajustarlo a "Last 90 days" para visualizar todos los datos disponibles. Esto es fundamental ya que de lo contrario las visualizaciones estarían vacías o mostrarían información incompleta.

---

## 7. Análisis crítico de las visualizaciones

Reflexiona sobre las visualizaciones creadas:

- **¿Cuál consideras más clara e informativa?**
  
  La visualización de "Ventas por Ciudad" es la más clara e informativa. Permite una comparación directa e inmediata entre las diferentes ciudades gracias al formato de barras verticales. El eje Y muestra claramente los valores monetarios y es fácil identificar cuál ciudad genera más ingresos con un simple vistazo.

- **¿Cuál podría inducir a error si se interpreta sin contexto?**
  
  La métrica de "Total de Ventas" podría inducir a error si se interpreta sin contexto temporal. Al ser un número absoluto sin referencia temporal clara, no se puede saber si corresponde a un día, semana o mes. Sin conocer que son 90 días de datos, alguien podría pensar que es un rendimiento diario o mensual, llevando a conclusiones incorrectas sobre el rendimiento del negocio.

- **¿Qué mejoras aplicarías (agregaciones, escalas, filtros, etc.)?**
  
  - Añadiría una visualización temporal (línea temporal) para ver la evolución de ventas a lo largo de los 90 días
  - Incorporaría un filtro interactivo por categoría de producto
  - Añadiría un gráfico de "donut" o "pie" para mostrar la distribución porcentual por estado (Completado, Pendiente, Cancelado)
  - Incluiría una tabla con el top 5 de vendedores
  - Añadiría colores consistentes para mejorar la identificación visual
  - Aplicaría un filtro para excluir ventas canceladas del análisis principal

---

## 8. Comparación con otras herramientas

Reflexiona brevemente:

1. **¿Qué ventajas ofrece Kibana frente a librerías de visualización en Python (Matplotlib, Seaborn, etc.)?**
   
   - **Interactividad inmediata**: Kibana permite explorar datos en tiempo real sin necesidad de ejecutar código cada vez
   - **No requiere programación**: Usuarios no técnicos (analistas de negocio, managers) pueden crear visualizaciones sin conocer Python
   - **Actualización automática**: Los dashboards se actualizan automáticamente con nuevos datos sin modificar código
   - **Filtros dinámicos**: Los usuarios pueden aplicar filtros y cambiar rangos temporales sin regenerar gráficos
   - **Integración nativa con Elasticsearch**: Optimizado para grandes volúmenes de datos
   - **Compartición fácil**: Los dashboards se pueden compartir mediante URL sin necesidad de exportar imágenes

2. **¿En qué situaciones preferirías usar una herramienta basada en código en lugar de Kibana?**
   
   - Cuando se necesitan **análisis estadísticos avanzados** (regresiones, clustering, machine learning)
   - Para **visualizaciones altamente personalizadas** que Kibana no soporta nativamente
   - En **procesos automatizados** que requieren integración con pipelines de datos
   - Para **generación de informes estáticos** en PDF o documentos
   - Cuando se trabaja con **múltiples fuentes de datos heterogéneas** no conectadas a Elasticsearch
   - En proyectos de **investigación o academia** donde se requiere reproducibilidad exacta del código
   - Para **manipulación compleja de datos** antes de la visualización

---

## 9. Uso futuro de las visualizaciones

Explica:

- **Qué visualización reutilizarías en un dashboard:**
  
  Reutilizaría las tres visualizaciones en un dashboard integrado, ya que se complementan bien:
  - La **métrica de Total Ventas** como KPI principal en la parte superior
  - **Ventas por Ciudad** para análisis geográfico
  - **Productos más vendidos** para análisis de inventario
  
  Además, añadiría una visualización temporal (evolución de ventas en el tiempo) y un gráfico de estado de pedidos para completar el cuadro de mando.

- **Qué tipo de usuario (técnico, analista, responsable) podría beneficiarse de cada visualización:**
  
  **Total Ventas (Métrica):**
  - **Responsables/Directores**: Para monitoreo rápido de KPIs y rendimiento global
  - **Analistas de negocio**: Como punto de partida para análisis más profundos
  
  **Ventas por Ciudad:**
  - **Responsables comerciales**: Para decisiones sobre distribución de recursos y estrategias regionales
  - **Analistas de marketing**: Para planificar campañas geográficamente segmentadas
  - **Directores de expansión**: Para identificar mercados potenciales
  
  **Productos más vendidos:**
  - **Responsables de compras/inventario**: Para gestión de stock y planificación de pedidos
  - **Analistas de producto**: Para identificar tendencias y productos estrella
  - **Equipo técnico/IT**: Para dimensionar infraestructura según demanda de productos

---

## 10. Dificultades encontradas (opcional)

Describe cualquier dificultad técnica o conceptual y cómo la has resuelto.

**Dificultades técnicas:**

1. **Rango temporal incorrecto**: Inicialmente las visualizaciones aparecían vacías porque el rango temporal por defecto estaba en "Last 15 minutes". Lo resolví ajustando el selector temporal a "Last 90 days" para coincidir con el período de datos generados.

2. **Selección del tipo de agregación**: Al principio no estaba claro si usar "Count" o "Sum" para las métricas. Comprendí que "Count" cuenta documentos mientras que "Sum" suma valores numéricos. Para ventas totales, "Sum of total" es más apropiado.

3. **Configuración inicial del Data View**: No sabía que era necesario crear un Data View antes de poder visualizar datos. Una vez creado con el patrón correcto (ventas*), todo funcionó correctamente.

**Dificultades conceptuales:**

1. **Diferencia entre Lens y otras visualizaciones**: Lens es la herramienta moderna y más intuitiva de Kibana, aunque también existen otras opciones más antiguas. Lens es la recomendada para la mayoría de casos de uso.

2. **Comprensión de agregaciones**: Entender cuándo usar cada tipo de agregación (terms, sum, avg, count) según el análisis deseado requirió experimentación.

Todas estas dificultades se resolvieron mediante exploración de la interfaz y consulta de la documentación básica de Kibana.

---

## 11. Reflexión final

Reflexiona brevemente (5–10 líneas):

- qué has aprendido en este laboratorio,
- la importancia de elegir correctamente el tipo de visualización,
- el papel de las visualizaciones en un proyecto Big Data real.

---

En este laboratorio he aprendido que **Kibana es una herramienta potente para democratizar el acceso a datos Big Data**, permitiendo que usuarios no técnicos puedan explorar y visualizar información sin necesidad de conocer lenguajes de programación o consultas complejas. La **importancia de elegir correctamente el tipo de visualización** es fundamental: un gráfico de barras es ideal para comparaciones, mientras que una métrica es perfecta para KPIs únicos, y elegir incorrectamente puede llevar a interpretaciones erróneas o confusión.

He comprendido que las visualizaciones no son un simple "adorno estético", sino una **herramienta de comunicación crítica en proyectos Big Data**. En un contexto real, los datos sin visualización adecuada son inútiles para la toma de decisiones, ya que los stakeholders no técnicos no pueden interpretar tablas de millones de registros. Kibana cierra el ciclo del pipeline Big Data: desde la ingesta y procesamiento hasta la presentación final de insights accionables.

La **capa de visualización transforma datos en decisiones**, y en entornos empresariales reales, un dashboard bien diseñado puede significar la diferencia entre detectar un problema a tiempo o descubrirlo demasiado tarde. Este laboratorio me ha mostrado cómo las herramientas modernas permiten análisis exploratorio ágil y dashboards interactivos que se actualizan en tiempo real, fundamental en la era del Big Data donde la velocidad de respuesta es competitiva.

---

## 12. Conclusión

Resume en 2–3 líneas qué aporta este laboratorio dentro de la UD3 y cómo conecta con el siguiente laboratorio.

---

Este laboratorio aporta la **capa de visualización y análisis exploratorio** que cierra el ciclo de datos iniciado en la UD2 (ingesta y procesamiento). Hemos aprendido a transformar datos almacenados en Elasticsearch en información visual comprensible mediante Kibana. Este conocimiento conecta directamente con el siguiente laboratorio donde profundizaremos en la **creación de dashboards analíticos más complejos**, incorporando múltiples visualizaciones interrelacionadas, filtros avanzados y análisis temporal para soportar la toma de decisiones estratégicas en tiempo real.

**CAPTURA 6: Dashboard completo con las 3 visualizaciones**
![CAPTURA 6 - Dashboard Ventas Lab1](Captura/captura6.png)

---

## Fin del documento de entrega