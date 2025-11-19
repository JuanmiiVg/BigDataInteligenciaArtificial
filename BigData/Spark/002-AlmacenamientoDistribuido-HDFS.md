### **Introducción a HDFS (Hadoop Distributed File System)**

El **Hadoop Distributed File System (HDFS)** es el sistema de archivos distribuido central del ecosistema Hadoop, diseñado específicamente para almacenar y procesar grandes volúmenes de datos en un entorno distribuido. Este sistema es fundamental en aplicaciones de Big Data, ya que permite manejar datos a escala de terabytes o petabytes de manera eficiente y fiable.

---

### **Características Clave de HDFS**

1. **Almacenamiento Distribuido**:
   - Los datos se dividen en bloques grandes (por defecto, 128 MB o más) que se distribuyen entre múltiples nodos dentro de un clúster.
   - Esta fragmentación permite que el procesamiento de los datos sea paralelizado, optimizando el rendimiento.

2. **Alta Disponibilidad y Tolerancia a Fallos**:
   - Cada bloque de datos se replica en varios nodos (por defecto, tres réplicas) para garantizar la disponibilidad incluso si un nodo falla.
   - Si un nodo que almacena datos falla, HDFS puede recuperar los datos de otros nodos donde se hayan replicado.

3. **Optimizado para Acceso Secuencial**:
   - Diseñado para leer y procesar grandes volúmenes de datos de manera secuencial en lugar de accesos aleatorios.
   - Esto lo hace ideal para aplicaciones que requieren análisis masivo, como el procesamiento de logs o análisis de datos transaccionales.

4. **Escalabilidad Horizontal**:
   - Se pueden añadir nodos al clúster para aumentar la capacidad de almacenamiento y procesamiento, sin necesidad de reconfiguraciones complejas.

5. **Integración con Ecosistemas Big Data**:
   - HDFS es compatible con herramientas como Apache Spark, Hive, Pig y HBase, lo que permite realizar análisis y consultas distribuidas.

---

### **Arquitectura de HDFS**

1. **NameNode (Nodo Maestro)**:
   - Es el componente principal que gestiona el metadato del sistema de archivos (ubicación de bloques, estructura de directorios, permisos, etc.).
   - Supervisa la disponibilidad de los nodos de datos, reparando automáticamente la pérdida de réplicas.

2. **DataNodes (Nodos de Datos)**:
   - Almacenan los bloques de datos reales distribuidos en todo el clúster.
   - Ejecutan operaciones de lectura y escritura bajo la dirección del NameNode.

3. **Secondary NameNode**:
   - Realiza copias periódicas del metadato del NameNode para asegurar la recuperación rápida en caso de fallo.

4. **Cliente HDFS**:
   - Los usuarios o aplicaciones interactúan con el NameNode para obtener información de ubicación de datos y se conectan a los DataNodes para leer o escribir los bloques.

---

### **Ventajas de HDFS**

- **Alta Fiabilidad**: Gracias a su sistema de replicación, los datos permanecen accesibles incluso si varios nodos fallan.
- **Escalabilidad**: Adecuado para entornos de Big Data en constante crecimiento.
- **Rendimiento Elevado**: Optimizado para el procesamiento paralelo de grandes conjuntos de datos.
- **Compatibilidad**: Integración fluida con herramientas analíticas y de procesamiento de datos como Spark y MapReduce.

---

### **Limitaciones de HDFS**

1. **No diseñado para datos pequeños**:
   - Maneja grandes archivos eficientemente, pero puede ser ineficiente para almacenar grandes cantidades de archivos pequeños debido al uso intensivo de metadatos.

2. **Latencia de Acceso**:
   - Optimizado para accesos secuenciales en lugar de aleatorios, lo que puede no ser ideal para aplicaciones OLTP (Procesamiento de Transacciones en Línea).

3. **Requiere Configuración Compleja**:
   - Configurar y administrar un clúster de HDFS requiere conocimientos técnicos avanzados.

---

### **Casos de Uso de HDFS**

1. **Procesamiento de Logs y Eventos**:
   - Ideal para almacenar y analizar grandes volúmenes de logs generados por servidores, aplicaciones o dispositivos IoT.

2. **Almacenamiento de Datos Empresariales**:
   - Empresas que manejan grandes volúmenes de datos transaccionales o de clientes.

3. **Análisis de Datos en la Nube**:
   - Almacenamiento de datos para aplicaciones de machine learning y análisis predictivo utilizando herramientas como Spark o Hive.

4. **Proyectos de Ciencia de Datos**:
   - Ofrece un repositorio centralizado para datos estructurados y no estructurados.

---

### **Conclusión**

HDFS es una solución poderosa y eficiente para el almacenamiento y procesamiento de datos en entornos distribuidos. Su diseño robusto y escalable lo convierte en una piedra angular para aplicaciones de Big Data, permitiendo que las organizaciones almacenen, gestionen y analicen datos masivos de manera fiable y económica.
### **Actividad en Clase: Usar HDFS con PySpark en AWS**

#### **Título de la Actividad:** Exploración Práctica de HDFS con PySpark en AWS

#### **Duración Aproximada:** 2-3 horas

#### **Objetivo:**
Introducir a los estudiantes al uso de **HDFS** (Hadoop Distributed File System) en un clúster de **Amazon EMR**, integrándolo con **PySpark** para cargar, procesar y guardar datos. Esta actividad práctica los guiará paso a paso mientras aprenden los fundamentos de almacenamiento distribuido y procesamiento paralelo.

---

### **Plan de Actividad**

#### **Introducción (20 minutos):**
1. Explica los conceptos básicos de HDFS:
   - Qué es HDFS y cómo funciona.
   - Importancia del almacenamiento distribuido en Big Data.
   - Rol de HDFS en entornos Hadoop y su integración con herramientas como PySpark.
2. Presenta Amazon EMR:
   - ¿Qué es EMR?
   - Cómo permite ejecutar Hadoop y Spark en AWS.
   - Introduce el entorno del Learner Lab de AWS Academy.

**Material de Apoyo:** Diapositivas con conceptos clave y diagramas del flujo de datos en HDFS.

---

### **Parte Práctica (2 horas)**

#### **Paso 1: Acceso al Learner Lab (15 minutos)**
1. Inicia sesión en AWS Academy Learner Lab:
   - Proporciona credenciales temporales generadas por el lab.
2. Instruye a los estudiantes a iniciar su entorno seleccionando **Start Lab** y a copiar las credenciales para iniciar sesión en AWS.

**Objetivo:** Garantizar que todos los estudiantes estén conectados al entorno AWS.

---

#### **Paso 2: Configuración de un Clúster EMR con HDFS (30 minutos)**
1. Dirige a los estudiantes al servicio **EMR**:
   - En la consola AWS, escribe "EMR" en la barra de búsqueda y selecciona el servicio.
2. Configuración básica del clúster:
   - Selecciona **Create cluster**.
   - Configura el clúster con:
     - **Release Version:** emr-6.9.0 o similar.
     - **Aplicaciones:** Seleccionar **Hadoop** y **Spark**.
     - **Instancias:** 1 nodo maestro y 2 nodos trabajadores (por defecto, `m5.xlarge`).
3. Inicia el clúster:
   - Haz clic en **Create cluster** y espera a que el estado cambie a **Running**.

**Objetivo:** Configurar un clúster funcional con HDFS habilitado.

---

#### **Paso 3: Acceso y Configuración de HDFS (20 minutos)**
1. Conectar al clúster:
   - Proporciona el comando SSH para conectar al nodo maestro desde la terminal.
   - Ejemplo de comando:
     ```bash
     ssh -i key.pem hadoop@<master-node-dns>
     ```
Con otras herramientas de AWS lo he conseguido desde mi ordenador, con esta sólo he conseguido conectar 
desde cloudshell.

2. Crear un directorio en HDFS:
   - Usar el comando:
     ```bash
     hdfs dfs -mkdir /user/data
     ```
3. Subir archivos a HDFS:
   - Proporciona un archivo de datos pequeño para cargar en HDFS (por ejemplo, `local_file.csv`).
   - Comando para subir el archivo:
     ```bash
     hdfs dfs -put local_file.csv /user/data/
     ```
4. Verificar el contenido del directorio:
   - Comando:
     ```bash
     hdfs dfs -ls /user/data/
     ```

**Objetivo:** Enseñar los comandos básicos para interactuar con HDFS.

---

#### **Paso 4: Uso de PySpark con HDFS (40 minutos)**
1. Iniciar el shell de PySpark:
   - Comando:
     ```bash
     pyspark
     ```
2. Leer datos desde HDFS:
   - Código:
     ```python
     df = spark.read.csv("hdfs:///user/data/Iris.csv", header=True)
     df.show()
     ```
3. Procesar los datos:
   - Ejemplo: Filtrar filas según una condición:
     ```python
     filtered_df = df.filter(df['Id'] > 100)
     filtered_df.show()
     ```
4. Guardar los resultados en HDFS:
   - Código:
     ```python
     filtered_df.write.csv("hdfs:///user/data/output.csv")
     ```

**Objetivo:** Realizar operaciones básicas de lectura, procesamiento y escritura de datos con PySpark en HDFS.

---

### **Cierre y Discusión (30 minutos)**
1. Repasa las actividades realizadas y discute:
   - ¿Qué dificultades encontraron?
   - ¿Cómo HDFS y PySpark ayudan en el procesamiento distribuido?
   - Casos prácticos donde estas herramientas podrían ser útiles.
2. Presenta ejemplos más avanzados para que los estudiantes continúen explorando:
   - Procesamiento en tiempo real con Spark Streaming.
   - Comparación de formatos de datos en HDFS.

---

### **Material Necesario**
1. Un archivo de datos de ejemplo para cargar en HDFS (puede ser un archivo CSV con datos ficticios).
2. Guía impresa o digital con comandos básicos de HDFS y PySpark.
3. Presentación introductoria con conceptos teóricos.

---

### **Evaluación**
Los estudiantes serán evaluados con base en:
- **Participación Activa:** Seguimiento de las instrucciones y ejecución de los pasos.
- **Configuración Correcta del Clúster EMR:** HDFS funcional con datos cargados.
- **Uso de PySpark:** Lectura, procesamiento y escritura de datos sin errores.
- **Reflexión Final:** Capacidad para identificar las ventajas y limitaciones de HDFS y PySpark.

Este enfoque práctico garantiza que los estudiantes entiendan no solo cómo configurar y usar HDFS en AWS, sino también su relevancia en proyectos reales de Big Data.
