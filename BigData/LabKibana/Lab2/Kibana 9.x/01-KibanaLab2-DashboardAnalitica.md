# UD3 — Laboratorio 2  
## Creación de visualizaciones con Kibana

---

### Módulo
Sistemas de Big Data

### Unidad Didáctica
UD3 — Procesamiento y visualización de datos en sistemas Big Data

### Laboratorio
Laboratorio 2 — Visualización de datos con Kibana

---

## 1. Objetivo del laboratorio

El objetivo de este laboratorio es **aprender a crear visualizaciones básicas en Kibana**, a partir de los datos previamente explorados en Discover, utilizando la **Visualize Library**.

Este laboratorio se centra en transformar datos en **representaciones gráficas comprensibles**, paso previo a la construcción de dashboards completos.

---

## 2. Relación con el laboratorio anterior

En el **Laboratorio 1** se ha trabajado:

- la exploración de datos con Discover,
- la identificación de campos relevantes,
- el guardado de búsquedas.

En este laboratorio se parte de ese conocimiento para **representar visualmente los datos**, manteniendo coherencia con lo ya analizado.

---

## 3. Entorno de trabajo

- Elasticsearch: **9.2.4**
- Kibana: **9.2.4**
- Despliegue: entorno local con Docker
- Seguridad avanzada: desactivada (entorno docente)

---

## 4. Acceso a la Visualize Library

1. Accede a Kibana en `http://localhost:5601`
2. En el menú lateral, ve a:

3. Pulsa **Create visualization**

Las visualizaciones creadas aquí se almacenan en la **biblioteca de visualizaciones** y podrán reutilizarse posteriormente en dashboards.

---

## 5. Selección del Data View

Al crear una nueva visualización:

1. Selecciona el **Data View** creado en el Laboratorio 1.
2. Comprueba que el rango temporal es correcto.
3. Asegúrate de que los datos coinciden con lo observado previamente en Discover.

---

## 6. Visualización 1 — Gráfico de barras

Crea un gráfico de barras que represente:

- una agregación (por ejemplo, número de eventos),
- agrupada por un campo categórico relevante.

Pasos orientativos:

- Tipo de visualización: **Bar**
- Métrica (Y): Count
- Dimensión (X): un campo categórico

👉 Guarda la visualización con un nombre descriptivo.

---

## 7. Visualización 2 — Gráfico temporal

Crea una visualización que muestre la evolución temporal de los datos:

- Tipo de visualización: **Line**
- Eje X: campo temporal
- Métrica: Count u otra métrica disponible

Observa cómo influyen los intervalos temporales en la visualización.

---

## 8. Visualización 3 — Tabla o métrica

Crea una tercera visualización, a elegir entre:

- una **tabla** con campos relevantes, o
- una **métrica** que muestre un valor agregado.

Esta visualización debe aportar información distinta a las anteriores.

---

## 9. Ajustes y configuración

Para cada visualización:

- ajusta títulos y etiquetas,
- revisa el rango temporal,
- comprueba que la visualización es coherente con los datos explorados.

Recuerda que una buena visualización **no es solo estética**, sino informativa.

---

## 10. Guardado en la Visualize Library

Asegúrate de que:

- todas las visualizaciones están guardadas,
- tienen nombres claros,
- pueden reutilizarse posteriormente en dashboards.

Estas visualizaciones serán utilizadas en el **Laboratorio 3**.

---

## 11. Análisis crítico de las visualizaciones

Reflexiona sobre las visualizaciones creadas:

- ¿Qué información aporta cada una?
- ¿Cuál resulta más clara?
- ¿Cuál podría inducir a error si se interpreta mal?

---

## 12. Comparación con otras herramientas

Reflexiona brevemente:

1. ¿Qué ventajas tiene Kibana frente a generar gráficos con Pandas o Matplotlib?
2. ¿En qué casos no usarías Kibana para visualizar datos?

---

## 13. Cierre del laboratorio

Este laboratorio sienta las bases para el siguiente paso:  
**integrar varias visualizaciones en dashboards** y construir cuadros de mando.

---

## Fin del Laboratorio 2