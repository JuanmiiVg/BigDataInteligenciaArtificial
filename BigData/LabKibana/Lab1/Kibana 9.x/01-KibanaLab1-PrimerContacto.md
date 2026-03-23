# UD3 — Laboratorio 1: Introducción a Kibana y visualización de datos

---

## 1. Objetivo del laboratorio

El objetivo de este laboratorio es **introducir Kibana como herramienta de exploración y visualización de datos** en entornos Big Data.

Al finalizar el laboratorio, el alumnado será capaz de:

- Comprender el papel de Kibana dentro de una arquitectura Big Data.
- Conectarse a un índice de datos en Elasticsearch.
- Explorar datos mediante **Discover**.
- Crear visualizaciones básicas.
- Construir un **dashboard sencillo**.
- Comparar Kibana con otras herramientas de visualización.

---

## 2. Contexto dentro de la UD3

Hasta ahora en la UD3 hemos trabajado:

- Ingesta e integración de datos (UD2).
- Calidad, limpieza y anonimización.
- Procesamiento paralelo con Spark.
- Análisis interactivo con Zeppelin.

En este punto:

👉 **Los datos ya están preparados**
👉 **No se procesan, se analizan y se muestran**

Kibana entra como **capa de visualización y análisis exploratorio**.

---

## 3. ¿Qué es Kibana?

Kibana es una herramienta de visualización y análisis de datos que forma parte del **Elastic Stack**.

Se utiliza principalmente para:

- Explorar grandes volúmenes de datos.
- Analizar eventos, logs y métricas.
- Crear dashboards interactivos.
- Monitorizar sistemas y procesos.

Kibana **no almacena datos**, sino que los consulta desde **Elasticsearch**.

---

## 4. Arquitectura simplificada

```text
Fuentes de datos
      ↓
Procesamiento (Spark)
      ↓
Elasticsearch
      ↓
Kibana
````

En este laboratorio **no se modifica Elasticsearch**, solo se consume.

---

## 5. Preparación del entorno

Se asume que ya están levantados:

* Elasticsearch
* Kibana

Y que existe al menos **un índice con datos** (por ejemplo `ventas`, `logs`, `eventos`…).

Accede a Kibana en el navegador:

```
http://localhost:5601
```

---

## 6. Primer contacto con Kibana

Al acceder a Kibana:

* Localiza el menú lateral izquierdo.
* Identifica las secciones principales:

  * **Discover**
  * **Visualize / Lens**
  * **Dashboard**
  * **Stack Management**

---

## 7. Paso 1 — Crear un Data View (Index Pattern)

Antes de explorar datos, Kibana necesita saber **qué índice usar**.

1. Ve a **Stack Management → Data Views**
2. Crea un nuevo Data View
3. Introduce:

   * Nombre del índice (por ejemplo `ventas*`)
4. Selecciona el campo de tiempo (si existe)
5. Guarda

👉 Este paso solo se hace una vez por índice.

---

## 8. Paso 2 — Exploración con Discover

Accede a **Discover**.

Aquí podrás:

* Ver documentos individuales.
* Examinar campos.
* Filtrar datos.
* Cambiar rangos temporales.

### Actividad guiada

* Aplica un filtro por algún campo (ej. ciudad, tipo, estado).
* Cambia el rango de fechas.
* Identifica:

  * número de documentos,
  * campos principales,
  * valores más frecuentes.

---

## 9. Paso 3 — Crear una visualización básica (Lens)

Accede a **Visualize → Lens**.

Crea una visualización sencilla:

Ejemplos:

* Número de registros por categoría.
* Suma de un campo numérico.
* Conteo por ciudad o tipo.

Guarda la visualización con un nombre claro.

---

## 10. Paso 4 — Crear un Dashboard

Accede a **Dashboard**.

1. Crea un nuevo dashboard.
2. Añade:

   * al menos 2 visualizaciones,
   * una tabla o métrica.
3. Ajusta el diseño.

👉 El objetivo no es estético, sino funcional.

---

## 11. Buenas prácticas con Kibana

* No crear dashboards con demasiadas visualizaciones.
* Usar nombres claros.
* Pensar en el **usuario final**.
* No duplicar información innecesaria.
* Validar filtros y rangos temporales.

---

## 12. Alternativas a Kibana (comparativa)

| Herramienta  | Uso principal            | Comentario                      |
| ------------ | ------------------------ | ------------------------------- |
| **Kibana**   | Logs, eventos, Big Data  | Muy integrada con Elasticsearch |
| **Grafana**  | Métricas, monitorización | Muy usada en DevOps             |
| **Power BI** | Análisis empresarial     | Orientada a negocio             |
| **Tableau**  | BI avanzado              | Muy potente, comercial          |
| **Superset** | BI open source           | Alternativa libre               |

👉 La herramienta se elige según el **contexto**, no por moda.

---

## 13. Preguntas de reflexión (para el alumnado)

Responde brevemente:

1. ¿Qué tipo de datos encajan mejor en Kibana?
2. ¿Qué ventajas ofrece frente a usar gráficos en Python?
3. ¿Qué limitaciones has encontrado?
4. ¿Usarías Kibana para informes de negocio? ¿Por qué?
5. ¿Qué herramienta elegirías para:

   * análisis técnico,
   * informes ejecutivos,
   * monitorización en tiempo real?

---

## 14. Evidencias para la entrega

Incluye en la entrega:

* Captura de Discover con filtros aplicados.
* Captura de una visualización creada.
* Captura del dashboard.
* Respuestas a las preguntas de reflexión.

---

## 15. Conclusión

Kibana permite transformar grandes volúmenes de datos en información comprensible de forma rápida.
En este laboratorio se ha trabajado la **visualización**, no el procesamiento, cerrando así el ciclo de datos iniciado en la UD2.

---

## Fin del Laboratorio 1 — Kibana
