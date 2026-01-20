# UD3 — Laboratorio 1: Primer contacto con Spark
## Documento de entrega del grupo

---

## 1. Datos del grupo

**Grupo:** Manuel Garrido, Israel Soto y Juan Manuel Vega
**Fecha de entrega:** 12 de enero de 2026

### Integrantes
- Alumno/a 1: Manuel Garrido
- Alumno/a 2: Israel Soto
- Alumno/a 3: Juan Manuel Vega

---

## 2. Objetivo del laboratorio

El objetivo de este laboratorio ha sido:

- Poner en marcha Apache Spark.
- Ejecutar un primer procesamiento distribuido.
- Comprender el modelo **Master / Worker**.
- Comparar conceptualmente Spark con pandas.

---

## 3. Entorno de ejecución utilizado

Marca la **opción final** que ha utilizado el grupo:

- ☑ **Plan A** — Clúster real (varias máquinas)
- ☐ **Plan B** — Master y Worker en una sola máquina
- ☐ **Plan C** — Spark en modo local (`local[*]`)

### Breve justificación
Explica por qué habéis usado esa opción (red, equipo, problemas técnicos, etc.):

> Hemos utilizado el Plan A con un clúster real distribuido en varias máquinas. Un compañero actuó como Master (IP 172.16.11.101) y otro como Worker (IP 172.16.11.115), conectados a través de la red LAN del aula. Esto nos permitió experimentar el funcionamiento real de un clúster distribuido Spark y comprender mejor la arquitectura Master-Worker.

---

## 4. Configuración básica del entorno

### Versión de Spark utilizada
- Apache Spark: **3.5.4**

### Rol de cada integrante
Indica qué rol ha tenido cada miembro del grupo:

- Manuel Garrido: ☐ Master ☑ Worker
- Israel Soto: ☑ Master ☐ Worker
- Juanma Vega: ☐ Master ☑ Worker

(Israel configuró el nodo Master en su máquina. Manuel y Juanma configuraron cada uno un Worker en sus respectivas máquinas, conectándose al Master para distribuir la carga de procesamiento).

---

## 5. Dataset utilizado

- Nombre del fichero: `ventas_clientes_anon.csv`
- Tipo de datos: Datos de ventas anonimizados
- Número aproximado de filas: Variable (dataset inflable según necesidades)
- Columnas principales: ciudad, importe, y otras métricas de ventas

> El dataset contiene información de ventas con datos de clientes anonimizados, incluyendo columnas como ciudad e importe de compra. Se utilizó para realizar análisis agregado de ventas por ciudad.

---

## 6. Descripción del procesamiento realizado

Resume **qué hace el programa Spark ejecutado** (`lab1_job.py`), en tus propias palabras:

- Lectura de datos: Carga del archivo CSV desde `/opt/spark-data/ventas_clientes_anon.csv` con inferencia automática de schema
- Filtro aplicado: Se filtran únicamente las ventas con importe superior a 100 unidades
- Agrupación realizada: Agrupación por ciudad
- Métricas calculadas: Número de ventas, importe total e importe medio por ciudad
- Tipo de salida generada: DataFrame ordenado por importe total descendente, mostrado en consola y guardado como CSV en `/opt/spark-data/output/ventas_por_ciudad`

> El job realiza un análisis de ventas por ciudad, filtrando transacciones significativas (>100), calculando estadísticas agregadas y generando un ranking de ciudades por volumen de ventas.

(No es necesario copiar código).

---

## 7. Problemas encontrados y cómo se resolvieron

Describe brevemente los problemas técnicos encontrados durante el laboratorio y cómo los solucionasteis.

Ejemplos:
- Problemas de red
- Problemas con Docker
- Workers que no conectaban
- Rutas incorrectas
- Otros

| Problema | Solución aplicada |
|--------|-------------------|
| Imagen Docker `bitnami/spark:3.5.4` no encontrada | Cambiamos a `apache/spark-py:latest` que sí estaba disponible en Docker Hub |
| Variable MASTER_IP no configurada inicialmente | Creamos archivo `.env` con `MASTER_IP=172.16.11.101` para persistencia |
| Permisos de escritura en `/opt/spark/work` | Añadimos volumen `./work:/opt/spark/work` en docker-compose.worker.yml |
| Worker mostraba Master URL como 0.0.0.0 en UI | Verificamos con `docker exec` que internamente usaba la IP correcta y confirmamos conexión en UI del Master |

---

## 8. Observaciones sobre Spark

Responde brevemente a las siguientes cuestiones:

### 8.1 ¿En qué se parece Spark a pandas?
> Spark se parece a pandas en la sintaxis de operaciones sobre DataFrames: filtrado con condiciones, agrupaciones (groupBy), funciones de agregación (sum, avg, count) y encadenamiento de operaciones. La API de Spark está inspirada en pandas para facilitar la transición.

### 8.2 ¿En qué se diferencia Spark de pandas?
> La principal diferencia es que Spark procesa datos de forma distribuida en múltiples nodos (lazy evaluation), mientras que pandas trabaja en memoria en una única máquina. Spark puede manejar datasets que no caben en memoria de un solo equipo, mientras que pandas está limitado por los recursos de una máquina.

### 8.3 ¿Qué ventaja principal aporta Spark en este laboratorio?
> La ventaja principal es la capacidad de procesamiento distribuido: el trabajo se reparte automáticamente entre el Master y los Workers, permitiendo procesar datasets grandes de forma paralela y escalable.

### 8.4 ¿Crees que Spark sería necesario para este dataset concreto? ¿Por qué?
> Para el dataset utilizado en este laboratorio probablemente no sea estrictamente necesario, ya que es relativamente pequeño y pandas podría manejarlo eficientemente. Sin embargo, si el dataset creciera significativamente (millones de registros) o necesitáramos procesar múltiples archivos simultáneamente, Spark se volvería imprescindible por su capacidad de escalar horizontalmente.

---

## 9. Evidencias de ejecución

Incluye **al menos una** de las siguientes evidencias:

- ☐ Captura de la UI de Spark Master (`:8080`)
- ☐ Captura de la ejecución del `spark-submit`
- ☐ Captura del resultado generado (`output/ventas_por_ciudad`)

(Pega aquí las imágenes o enlázalas).

---

## 10. Conclusión del grupo

Redacta una breve conclusión (5–8 líneas) respondiendo a:

> ¿Qué has aprendido sobre Spark y el procesamiento distribuido en este laboratorio?
(Cada miembro del equipo explica brevemente lo que ha aprendido)
> 
> **Manuel Garrido**: He entendido el rol del Worker en un clúster Spark, cómo se conecta al Master y ejecuta las tareas asignadas de forma automática. También he aprendido a diagnosticar problemas de conectividad y configuración en Docker.
> 
> **Israel Soto**: He aprendido a configurar y gestionar un nodo Master de Spark, comprendiendo cómo coordina el trabajo entre workers y distribuye las tareas de procesamiento.
> 
> **Juanma Vega**: Como segundo Worker, he comprendido cómo múltiples nodos worker colaboran en paralelo para procesar un mismo job, experimentando directamente la escalabilidad horizontal de Spark y la distribución de carga entre nodos.
>
> Como grupo, hemos experimentado directamente las ventajas del procesamiento distribuido y la escalabilidad horizontal que ofrece Spark, comprendiendo cuándo es apropiado usar esta tecnología.

---

## 11. Valoración del trabajo en grupo (opcional)

- Reparto de tareas: El reparto fue efectivo, con roles claros (Master, Worker, documentación). Cada miembro contribuyó según su rol asignado.
- Dificultades de coordinación: Encontramos algunos desafíos al sincronizar las IPs y verificar la conectividad entre máquinas. La comunicación constante fue clave para resolver problemas.
- Qué mejoraríais en el próximo laboratorio: Preparar mejor el entorno previo (verificar imágenes Docker disponibles, configurar red de antemano) y documentar paso a paso desde el inicio para facilitar la resolución de problemas.

> El trabajo en grupo fue positivo, con buena comunicación y colaboración. Aprendimos tanto de los aciertos como de los errores técnicos encontrados.
