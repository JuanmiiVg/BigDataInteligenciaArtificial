# UD3 — Laboratorio 3  
## Creación de dashboards con Kibana

---

### Módulo
Sistemas de Big Data

### Unidad Didáctica
UD3 — Procesamiento y visualización de datos en sistemas Big Data

### Laboratorio
Laboratorio 3 — Construcción de dashboards con Kibana

---

## 1. Objetivo del laboratorio

El objetivo de este laboratorio es **integrar visualizaciones previamente creadas en un dashboard**, utilizando Kibana como herramienta para la **presentación conjunta y contextualizada de la información**.

Un dashboard permite **obtener una visión global del sistema o del conjunto de datos**, y está orientado a usuarios que necesitan interpretar información de forma rápida y visual.

---

## 2. Relación con los laboratorios anteriores

En los laboratorios previos se ha trabajado:

- **Lab 1:** exploración de datos con Discover.
- **Lab 2:** creación de visualizaciones en la Visualize Library.

En este laboratorio se reutilizan esas visualizaciones para **construir dashboards**, sin crear gráficos nuevos desde cero.

---

## 3. Entorno de trabajo

- Elasticsearch: **9.2.4**
- Kibana: **9.2.4**
- Despliegue: entorno local con Docker
- Seguridad avanzada: desactivada (entorno docente)

---

## 4. Acceso a Dashboards

1. Accede a Kibana en `http://localhost:5601`
2. En el menú lateral, ve a:

3. Pulsa **Create dashboard**

---

## 5. Añadir visualizaciones al dashboard

1. Dentro del dashboard, pulsa **Add from library**
2. Selecciona las visualizaciones creadas en el Laboratorio 2.
3. Añade al menos **tres visualizaciones**.

Las visualizaciones se pueden:
- mover,
- redimensionar,
- reorganizar libremente.

---

## 6. Organización del dashboard

Organiza el dashboard de forma coherente:

- coloca las visualizaciones más importantes en la parte superior,
- agrupa visualizaciones relacionadas,
- evita la sobrecarga visual.

El objetivo no es llenar la pantalla, sino **comunicar información**.

---

## 7. Uso de filtros y controles

Dentro del dashboard:

- ajusta el **rango temporal global**,
- comprueba cómo afectan los filtros a todas las visualizaciones,
- observa la coherencia entre gráficos al aplicar cambios.

Este comportamiento es clave para dashboards reales.

---

## 8. Guardado del dashboard

1. Guarda el dashboard.
2. Asigna un nombre claro y descriptivo.
3. Comprueba que puede abrirse correctamente desde la lista de dashboards.

---

## 9. Análisis del dashboard

Reflexiona sobre el dashboard creado:

- ¿Qué información principal se obtiene de un vistazo?
- ¿Qué visualización es más relevante?
- ¿Qué información queda menos clara?

---

## 10. Comparación con otros tipos de cuadros de mando

Reflexiona brevemente:

1. ¿En qué se diferencia este dashboard de un cuadro de mando de negocio?
2. ¿Qué tipo de usuario usaría este dashboard?
3. ¿Qué limitaciones tiene Kibana frente a herramientas de BI tradicionales?

---

## 11. Buenas prácticas en dashboards

Ten en cuenta:

- menos visualizaciones suelen ser más efectivas,
- títulos claros y descriptivos,
- coherencia en escalas y colores,
- uso adecuado del tiempo como eje común.

---

## 12. Cierre del laboratorio

Este laboratorio completa el flujo:

**explorar → visualizar → integrar**

y cierra el bloque de trabajo con Kibana dentro de la UD3.

---

## Fin del Laboratorio 3