
# UD3 — Laboratorio 2: Dashboards y análisis con Kibana

---

## 1. Objetivo del laboratorio

El objetivo de este laboratorio es **profundizar en el uso de Kibana para el análisis y la presentación de información**, centrándonos en:

- Diseño de dashboards con sentido analítico.
- Uso de filtros globales e interacciones.
- Comparación de métricas y dimensiones.
- Interpretación de resultados.
- Pensar en Kibana como herramienta de apoyo a la toma de decisiones.

---

## 2. Relación con el laboratorio anterior

En el **Laboratorio 1** se ha trabajado:

- Exploración básica con Discover.
- Creación de visualizaciones simples.
- Construcción de un dashboard básico.

En este laboratorio:

👉 **No se aprende Kibana nuevo**,  
👉 **se aprende a usarlo mejor**.

El foco pasa de la herramienta al **análisis**.

---

## 3. Contexto de trabajo

Se parte de:

- Datos ya procesados y limpios.
- Datos almacenados en Elasticsearch.
- Al menos un índice funcional (por ejemplo `ventas`, `eventos`, `logs`, etc.).

No se modifica el índice ni los datos.

---

## 4. Recordatorio: buenas preguntas antes de visualizar

Antes de crear visualizaciones, reflexiona:

- ¿Qué quiero saber?
- ¿Para quién es este dashboard?
- ¿Qué decisiones podría tomar alguien con esta información?

👉 Un buen dashboard responde preguntas, no solo muestra gráficos.

---

## 5. Actividad 1 — Análisis guiado con Discover

Accede a **Discover** y realiza lo siguiente:

1. Aplica al menos **dos filtros combinados**.
2. Cambia el rango temporal.
3. Identifica:
   - un valor dominante,
   - un posible pico o anomalía,
   - un campo poco informativo.

Describe brevemente tus observaciones.

---

## 6. Actividad 2 — Visualizaciones comparativas

Crea al menos **dos visualizaciones** que permitan **comparar datos**, por ejemplo:

- Comparación entre categorías.
- Evolución temporal de una métrica.
- Distribución porcentual.

Recomendaciones:
- Usa títulos claros.
- Evita gráficos innecesariamente complejos.
- Piensa en qué aporta cada visualización.

Guarda las visualizaciones.

---

## 7. Actividad 3 — Uso de filtros en el dashboard

Crea un nuevo dashboard o reutiliza uno existente.

Incluye:

- Un **control de filtro** (por ejemplo por categoría, ciudad, tipo, etc.).
- Al menos **dos visualizaciones afectadas por ese filtro**.

Comprueba que:
- Al cambiar el filtro, todas las visualizaciones se actualizan.
- El dashboard sigue siendo comprensible.

---

## 8. Actividad 4 — Dashboard con objetivo definido

Diseña un dashboard con un **objetivo claro**, por ejemplo:

- Seguimiento de actividad.
- Análisis de comportamiento.
- Control de un proceso.
- Resumen ejecutivo.

Describe brevemente:
- A quién va dirigido.
- Qué decisiones permite tomar.

👉 No se valora el diseño gráfico, sino la coherencia.

---

## 9. Interpretación de resultados

Responde a las siguientes cuestiones:

1. ¿Qué información relevante se obtiene del dashboard?
2. ¿Hay algún patrón claro en los datos?
3. ¿Qué información falta para mejorar el análisis?
4. ¿Qué errores se podrían cometer interpretando mal estos gráficos?

---

## 10. Comparativa con otras herramientas

Reflexiona brevemente:

- ¿Qué tipo de análisis sería mejor hacer con Spark o Python?
- ¿Qué tipo de análisis encaja mejor con Kibana?
- ¿Qué ventajas tiene Kibana en tiempo real frente a herramientas de BI clásico?

---

## 11. Buenas prácticas reforzadas

- Un dashboard no es un mural de gráficos.
- Menos visualizaciones bien pensadas > muchas sin sentido.
- El contexto es tan importante como el dato.
- Los filtros son parte del análisis, no un añadido.

---

## 12. Evidencias para la entrega

Para la entrega del laboratorio se deberá incluir:

- Captura de Discover con filtros.
- Captura de al menos dos visualizaciones comparativas.
- Captura del dashboard con filtros.
- Respuestas a las preguntas de interpretación.

---

## 13. Conclusión

Este laboratorio refuerza la idea de que **visualizar datos es una parte clave del sistema Big Data**, pero siempre debe ir acompañada de análisis crítico y comprensión del contexto.

---

## Fin del Laboratorio 2 — Kibana

