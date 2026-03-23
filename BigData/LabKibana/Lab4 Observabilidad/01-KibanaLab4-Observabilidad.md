# UD3 — Laboratorio de ampliación: Observabilidad con Kibana
## Logs, métricas y monitorización de sistemas

---

## 1. Naturaleza del laboratorio

Este laboratorio se plantea como **ampliación o cierre técnico alternativo** de la UD3.

No sustituye a los Laboratorios 1, 2 y 3 de Kibana, sino que muestra **otro uso real de Kibana**:  
👉 **la observabilidad técnica de sistemas**.

Su realización puede ser:
- voluntaria,
- opcional,
- o propuesta como alternativa al Laboratorio 3 de análisis de negocio.

---

## 2. Objetivo del laboratorio

El objetivo de este laboratorio es **comprender el concepto de observabilidad** y el papel de Kibana como herramienta para:

- analizar logs,
- explorar métricas técnicas,
- detectar problemas de funcionamiento,
- monitorizar sistemas y servicios.

Al finalizar el laboratorio, el alumnado será capaz de:

- diferenciar entre análisis de datos y observabilidad,
- explorar logs en Kibana,
- interpretar métricas técnicas básicas,
- comprender cómo se monitorizan sistemas en entornos reales.

---

## 3. Contexto dentro de la UD3

En la UD3 se ha trabajado principalmente:

- procesamiento de datos con Spark,
- análisis y exploración de datos,
- visualización orientada a análisis.

Este laboratorio introduce un **caso de uso distinto**:

| Análisis de datos | Observabilidad |
|------------------|---------------|
| Datos de negocio | Datos técnicos |
| Informes y dashboards | Diagnóstico y monitorización |
| Decisiones estratégicas | Detección de problemas |
| Usuario analista | Usuario técnico / DevOps |

---

## 4. ¿Qué es la observabilidad?

La observabilidad es la capacidad de **entender qué está ocurriendo dentro de un sistema** a partir de los datos que genera.

Se basa principalmente en:
- **logs** (registros de eventos),
- **métricas** (uso de recursos, contadores),
- **eventos** (errores, alertas).

Kibana es una herramienta ampliamente utilizada para este fin.

---

## 5. Escenario de trabajo

En este laboratorio se trabaja con:

- Elasticsearch y Kibana ya configurados.
- Índices que contienen:
  - logs de aplicaciones,
  - métricas de sistema,
  - eventos técnicos simulados o reales.
- Dashboards y visualizaciones preconfiguradas.

El objetivo **no es crear datos**, sino **interpretarlos**.

---

## 6. Preparación del entorno

El entorno se prepara mediante un script de arranque proporcionado (`bootstrap_kibana_lab.sh`), que:

- levanta los servicios necesarios,
- carga datos de ejemplo,
- configura índices y dashboards.

El alumnado **no debe modificar el script**, solo ejecutarlo y comprobar que los servicios están activos.

---

## 7. Exploración inicial con Discover

Accede a **Discover** y realiza las siguientes tareas:

1. Selecciona un índice de logs.
2. Explora los documentos disponibles.
3. Identifica:
   - tipos de mensajes,
   - niveles de log (info, warning, error),
   - campos más frecuentes.

Aplica filtros para:
- mostrar solo errores,
- limitar por rango temporal.

---

## 8. Análisis de métricas

Accede a las visualizaciones o dashboards de métricas.

Analiza:
- uso de CPU o memoria,
- número de eventos por unidad de tiempo,
- evolución temporal de alguna métrica.

Reflexiona:
- ¿hay picos?
- ¿hay comportamientos anómalos?
- ¿qué podría estar ocurriendo en el sistema?

---

## 9. Dashboards de observabilidad

Explora los dashboards disponibles.

Describe:
- qué información muestra cada uno,
- qué problema técnico ayudaría a detectar,
- qué usuario los utilizaría (desarrollador, administrador, etc.).

---

## 10. Análisis e interpretación (parte clave)

Responde a las siguientes cuestiones:

1. ¿Qué tipo de problemas se podrían detectar con estos datos?
2. ¿Qué diferencia hay entre analizar logs y analizar datos de negocio?
3. ¿Qué información consideras más importante en un dashboard de observabilidad?
4. ¿Qué información falta para un diagnóstico más preciso?

---

## 11. Comparación con otros usos de Kibana

Reflexiona brevemente:

- ¿En qué se diferencia este uso de Kibana del trabajado en los Labs 1–3?
- ¿Por qué no tendría sentido usar Kibana de observabilidad como cuadro de mando de negocio?
- ¿Qué tipo de perfiles profesionales trabajarían con este tipo de dashboards?

---

## 12. Limitaciones del laboratorio

Indica algunas limitaciones del laboratorio, por ejemplo:

- datos simulados,
- falta de alertas automáticas,
- ausencia de trazas distribuidas,
- simplificación del sistema real.

---

## 13. Evidencias para la entrega

En caso de realizar este laboratorio, la entrega debe incluir:

- captura de Discover con filtros aplicados,
- captura de algún dashboard de observabilidad,
- respuestas a las preguntas de análisis e interpretación.

---

## 14. Conclusión

Este laboratorio muestra un uso alternativo y real de Kibana como herramienta de observabilidad, complementando el análisis de datos trabajado en la UD3 y reforzando la visión global de los sistemas Big Data.

---

## Fin del laboratorio de observabilidad

