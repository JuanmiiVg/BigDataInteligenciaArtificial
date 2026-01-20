# UD3 — Laboratorio 2: Spark frente a pandas
## Documento de entrega del grupo

---

## 1. Datos del grupo

**Grupo:** Big Data Cluster - Spark Lab 2  
**Fecha de entrega:** 15 de enero de 2026

### Integrantes
- **Master:** Israel Soto
- **Worker 1:** Juan Manuel Vega
- **Worker 2:** Manuel Garrido

---

## 2. Objetivo del laboratorio

El objetivo de este laboratorio ha sido:

- Aumentar artificialmente el volumen de datos.
- Procesar el mismo dataset con **pandas** y con **Spark**.
- Observar cómo afecta el volumen al tiempo y a la experiencia de uso.
- Reflexionar sobre **cuándo tiene sentido Spark** y cuándo no.

---

## 3. Dataset utilizado

### Dataset base
- Nombre: ventas_clientes_anon.csv
- Número aproximado de filas: 4
- Tamaño aproximado: 120 bytes

### Dataset inflado
- Factor de inflado aplicado: 100×
- Número aproximado de filas final: 400
- Tamaño aproximado final: 12 KB

> No fue necesario reducir el factor. Con 400 filas manejamos cómodamente el volumen.

---

## 4. Ejecución con pandas

### Resultado general
Describe brevemente cómo ha sido la ejecución con pandas:

- ☑ Rápida y fluida  
- ☐ Lenta pero funcional  
- ☐ Muy lenta / problemática  
- ☐ No se pudo completar  

### Observaciones
Comenta cualquier aspecto relevante:
- consumo de memoria: Mínimo (~50 MB)
- tiempo de espera: 0.03 segundos
- bloqueos: Ninguno
- sensación general: Excelente rendimiento

---

## 5. Ejecución con Spark

### Modo de ejecución
Marca la opción utilizada:

- ☐ Plan A — Clúster real (varias máquinas)
- ☑ Plan B — Master y Worker en una sola máquina
- ☐ Plan C — Spark local

### Observaciones
Describe cómo se ha comportado Spark con el mismo volumen de datos:

- tiempo aproximado: 8-12 segundos
- estabilidad: Perfecta
- uso de CPU: Distribuido en 2 workers
- diferencias: Spark 300× más lento

---

## 6. Preguntas de reflexión (obligatorias)

Responde de forma clara y razonada a las siguientes preguntas.

---

### 6.1 ¿Qué ha pasado al aumentar el volumen de datos?

Al aumentar de 4 a 400 registros (100×), pandas mantuvo prácticamente el mismo tiempo (0.03s). Spark también procesó eficientemente, pero el overhead de iniciar el cluster fue el factor dominante.

---

### 6.2 ¿En qué momento pandas empieza a ser incómodo?

Pandas empieza a ser incómodo cuando: (1) los datos ocupan >80% de la RAM disponible; (2) necesitas procesar datos distribuidos; (3) requieres procesamiento en tiempo real. Con 8 GB de RAM, el punto crítico está alrededor de 1 GB de datos.

---

### 6.3 ¿Spark es siempre mejor que pandas? ¿Por qué?

No. Son herramientas complementarias. Pandas gana en pequeño volumen y velocidad. Spark gana en escalabilidad y procesamiento distribuido. En este laboratorio con 400 filas, pandas fue 300× más rápido. Pero con 1 TB distribuido, Spark sería imprescindible.

---

### 6.4 ¿Qué coste tiene usar Spark frente a pandas?

Complejidad técnica muy alta. Recursos: múltiples máquinas (~$500-2000/mes en cloud). Desarrollo 3-5× más lento. Mantenimiento: alto (monitoreo, logs). El beneficio solo se justifica con volúmenes muy grandes.

---

### 6.5 ¿Qué enfoque usarías en cada caso?

#### a) Un análisis rápido exploratorio
pandas + Jupyter. Necesitas respuestas en minutos, típicamente <5 GB.

#### b) Un proceso periódico (diario, semanal…)
pandas si <1 GB, Spark si >1 GB distribuido.

#### c) Un volumen de datos muy grande
Spark + HDFS. Terabytes/petabytes, infraestructura distribuida ya existe.

---

## 7. Comparación final (resumen)

Completa esta tabla con tus conclusiones:

| Aspecto | pandas | Spark |
|------|------|------|
| Facilidad de uso | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Escalabilidad | ⭐ | ⭐⭐⭐⭐⭐ |
| Consumo de recursos | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Adecuado para Big Data | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 8. Conclusión del grupo

Este laboratorio nos enseñó que no existe herramienta universalmente mejor, sino herramientas para problemas específicos. Pandas es perfecta para análisis rápido (0.03s en nuestro test), Spark existe para volúmenes exponenciales. En producción, ambas coexisten: pandas para prototipado, Spark para pipelines masivos. Aprendimos a elegir la herramienta correcta según el problema.

---

## 9. Dificultades técnicas (si las hubo)

- Problema: La red.
- Solución: Paciencia.

---

## 10. Valoración del trabajo en grupo (opcional)

- Reparto de tareas: Israel, Juan Manuel, Manuel
- Coordinación: Excelente, roles claros facilitaron colaboración
- Mejoras: Scripts automatizados