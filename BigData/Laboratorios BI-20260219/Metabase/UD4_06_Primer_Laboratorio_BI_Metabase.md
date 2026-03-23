# UD4 - Laboratorio 1
## Creacion de un cuadro de mando en Metabase

---

## 1. Objetivo del laboratorio

En este laboratorio el alumnado debera:

- Conectar Metabase a la base de datos preparada.
- Crear preguntas utilizando la interfaz grafica.
- Diseñar un dashboard coherente.
- Justificar las metricas utilizadas.
- Interpretar los resultados obtenidos.

No se evaluara la estetica avanzada.
Se evaluara la coherencia analitica.

---

## 2. Contexto

Partimos de:

- Dataset limpio.
- Tablas estructuradas.
- Vistas agregadas si fuera necesario.

No esta permitido:

- Modificar la base de datos sin justificarlo.
- Crear metricas arbitrarias sin explicacion.

---

## 3. Parte A - Conexion y exploracion

### 3.1 Conexion

- Conectar Metabase a la base de datos PostgreSQL.
- Verificar que las tablas son visibles.
- Identificar tabla de hechos y tablas de dimensiones.

### 3.2 Exploracion inicial

Responder:

1. ¿Cual es la tabla principal?
2. ¿Cual es su granularidad?
3. ¿Que columnas representan metricas?
4. ¿Que columnas representan dimensiones?

---

## 4. Parte B - Creacion de preguntas

Se deben crear al menos 3 preguntas guardadas.

### Pregunta 1 - Evolucion temporal

Requisitos:

- Agregacion temporal por mes o semana.
- Suma o media de una metrica principal.
- Visualizacion en grafico de lineas.

### Pregunta 2 - Comparacion por categoria

Requisitos:

- Agrupacion por categoria relevante.
- Visualizacion en grafico de barras.
- Orden descendente por valor.

### Pregunta 3 - Indicador clave (KPI)

Requisitos:

- Valor numerico unico.
- Puede ser suma total, media o ratio.
- Visualizacion tipo indicador.

Cada pregunta debe:

- Tener nombre claro.
- Estar guardada.

---

## 5. Parte C - Creacion del dashboard

El dashboard debe incluir:

- Las 3 preguntas anteriores.
- Disposicion ordenada.
- Titulos descriptivos.
- Al menos un filtro global (si procede).

El dashboard debe responder a una pregunta de negocio clara.

Ejemplo:

- ¿Como evoluciona la actividad?
- ¿Que categoria domina?
- ¿Cual es el rendimiento global?

---

## 6. Parte D - Interpretacion

El informe debe incluir:

1. ¿Que patrones se observan?
2. ¿Existen picos o anomalías?
3. ¿Que categoria tiene mayor impacto?
4. ¿Que decision podria tomarse a partir del dashboard?

No basta describir el grafico.
Se debe interpretar.

---

## 7. Parte E - Reflexion tecnica

Responder:

1. ¿Se utilizo agregacion correcta?
2. ¿Se podria mejorar el modelo de datos?
3. ¿Seria necesario preagregar si el volumen creciera?
4. ¿Se mezclaron granularidades distintas?

---

## 8. Entregable

Documento markdown/docx/

PDF con:

- Capturas de las preguntas creadas.
- Captura del dashboard final.
- Respuestas razonadas.
- Justificacion de las metricas.

No se aceptaran entregas sin interpretacion.

---

## 9. Criterios de evaluacion

Se evaluara:

- Correcta conexion y uso de datos.
- Coherencia de agregaciones.
- Calidad de interpretacion.
- Claridad del dashboard.
- Capacidad de reflexion tecnica.

---

## 10. Extension opcional

Opcional para subir nota:

- Crear una cuarta visualizacion comparativa.
- Implementar filtro dinamico avanzado.
- Proponer mejora del modelo SQL.

---

## Fin del laboratorio
