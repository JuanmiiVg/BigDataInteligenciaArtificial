# ============================================================================
# PRÁCTICA HDFS CON PYSPARK EN AWS EMR
# Exploración Práctica de HDFS con PySpark en AWS
# ============================================================================
# Duración: 2-3 horas
# Objetivo: Aprender a usar HDFS en Amazon EMR integrándolo con PySpark
# ============================================================================

"""
REQUISITOS PREVIOS:
-------------------
1. Acceso a AWS Academy Learner Lab
2. Clúster EMR configurado con Hadoop y Spark
3. Conexión SSH al nodo maestro (o uso de CloudShell)

ESTRUCTURA DE LA PRÁCTICA:
---------------------------
PARTE 1: Comandos HDFS (Terminal SSH)
PARTE 2: Trabajo con PySpark
PARTE 3: Cierre y Discusión
"""

# ============================================================================
# PARTE 1: COMANDOS HDFS
# ============================================================================
# Ejecutar estos comandos en la terminal SSH del nodo maestro EMR

"""
# ----------------------------------------------------------------------------
# PASO 3.1: CREAR DIRECTORIO EN HDFS
# ----------------------------------------------------------------------------

# Crear directorio para almacenar datos
hdfs dfs -mkdir /user/data

# Verificar que se creó correctamente
hdfs dfs -ls /user/


# ----------------------------------------------------------------------------
# PASO 3.2: CREAR Y SUBIR ARCHIVO A HDFS
# ----------------------------------------------------------------------------

# Crear un archivo CSV de ejemplo en el sistema local
cat > local_file.csv << 'EOF'
id,nombre,edad,ciudad,salario
1,Juan,28,Madrid,45000
2,María,34,Barcelona,52000
3,Carlos,45,Valencia,48000
4,Ana,29,Sevilla,41000
5,Pedro,38,Bilbao,55000
6,Laura,31,Málaga,43000
7,Miguel,42,Zaragoza,50000
8,Carmen,27,Murcia,39000
9,David,36,Palma,47000
10,Elena,33,Granada,44000
EOF

# Verificar que el archivo se creó localmente
ls -lh local_file.csv
cat local_file.csv


# ----------------------------------------------------------------------------
# PASO 3.3: SUBIR ARCHIVO A HDFS
# ----------------------------------------------------------------------------

# Subir el archivo desde local a HDFS
hdfs dfs -put local_file.csv /user/data/

# Verificar que se subió correctamente
hdfs dfs -ls /user/data/

# Ver el contenido del archivo en HDFS
hdfs dfs -cat /user/data/local_file.csv


# ----------------------------------------------------------------------------
# COMANDOS ÚTILES DE HDFS (Referencia rápida)
# ----------------------------------------------------------------------------

# Listar contenido de un directorio
hdfs dfs -ls /user/data/

# Ver las primeras líneas de un archivo
hdfs dfs -head /user/data/local_file.csv

# Ver el contenido completo de un archivo
hdfs dfs -cat /user/data/local_file.csv

# Copiar archivo dentro de HDFS
hdfs dfs -cp /user/data/local_file.csv /user/data/backup.csv

# Mover/renombrar archivo en HDFS
hdfs dfs -mv /user/data/backup.csv /user/data/respaldo.csv

# Descargar archivo de HDFS a local
hdfs dfs -get /user/data/local_file.csv ./archivo_descargado.csv

# Eliminar archivo de HDFS
hdfs dfs -rm /user/data/respaldo.csv

# Crear directorio adicional
hdfs dfs -mkdir /user/data/temp

# Eliminar directorio vacío
hdfs dfs -rmdir /user/data/temp

# Eliminar directorio con contenido (recursivo)
hdfs dfs -rm -r /user/data/temp/

# Ver espacio usado en HDFS
hdfs dfs -du -h /user/data/

# Ver información detallada de replicación
hdfs fsck /user/data/local_file.csv -files -blocks -locations

# Ver estadísticas del sistema HDFS
hdfs dfsadmin -report
"""

# ============================================================================
# PARTE 2: TRABAJO CON PYSPARK
# ============================================================================
# Ejecutar estos comandos después de iniciar PySpark con el comando: pyspark

print("="*80)
print("PARTE 2: TRABAJO CON PYSPARK")
print("="*80)

# ----------------------------------------------------------------------------
# PASO 4.1: INICIALIZACIÓN Y CONFIGURACIÓN
# ----------------------------------------------------------------------------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, when, sum as spark_sum, max as spark_max

# Crear sesión de Spark (si no está ya iniciada)
spark = SparkSession.builder \
    .appName("HDFS_PySpark_Practice") \
    .getOrCreate()

# Verificar la configuración
print("\n" + "="*80)
print("CONFIGURACIÓN DE SPARK")
print("="*80)
print(f"Versión de Spark: {spark.version}")
print(f"Master: {spark.sparkContext.master}")
print(f"App Name: {spark.sparkContext.appName}")

# ----------------------------------------------------------------------------
# PASO 4.2: LEER DATOS DESDE HDFS
# ----------------------------------------------------------------------------

print("\n" + "="*80)
print("PASO 4.2: LEER DATOS DESDE HDFS")
print("="*80)

# Leer el archivo CSV desde HDFS
df = spark.read.csv("hdfs:///user/data/local_file.csv", header=True, inferSchema=True)

# Mostrar los primeros registros
print("\n📊 DATOS ORIGINALES:")
df.show()

# Ver el esquema de datos
print("\n📋 ESQUEMA DE DATOS:")
df.printSchema()

# Información básica del DataFrame
print("\n📈 INFORMACIÓN BÁSICA:")
print(f"Número total de registros: {df.count()}")
print(f"Número de columnas: {len(df.columns)}")
print(f"Columnas: {df.columns}")

# Estadísticas descriptivas
print("\n📊 ESTADÍSTICAS DESCRIPTIVAS:")
df.describe().show()

# ----------------------------------------------------------------------------
# PASO 4.3: PROCESAR LOS DATOS (FILTROS Y TRANSFORMACIONES)
# ----------------------------------------------------------------------------

print("\n" + "="*80)
print("PASO 4.3: PROCESAR LOS DATOS")
print("="*80)

# Ejemplo de filtro: Empleados con salario mayor a 45000
print("\n🔍 FILTRO: Empleados con salario > 45000")
filtered_df = df.filter(col("salario") > 45000)
filtered_df.show()

print(f"Total de empleados con salario > 45000: {filtered_df.count()}")

# Seleccionar columnas específicas
print("\n📌 SELECCIÓN DE COLUMNAS (nombre y salario):")
df.select("nombre", "salario").show()

# Ordenar por salario descendente
print("\n📊 EMPLEADOS ORDENADOS POR SALARIO (DESCENDENTE):")
df.orderBy(col("salario").desc()).show()

# Crear una nueva columna con categoría de salario
print("\n➕ CREAR NUEVA COLUMNA: Categoría de salario")
df_with_category = df.withColumn(
    "categoria_salario",
    when(col("salario") < 42000, "Bajo")
    .when((col("salario") >= 42000) & (col("salario") < 48000), "Medio")
    .otherwise("Alto")
)
df_with_category.show()

# Filtro múltiple: Empleados mayores de 30 años con salario alto
print("\n🔍 FILTRO MÚLTIPLE: Edad > 30 Y Salario > 47000")
df.filter((col("edad") > 30) & (col("salario") > 47000)).show()

# ----------------------------------------------------------------------------
# PASO 4.4: ANÁLISIS Y AGREGACIONES
# ----------------------------------------------------------------------------

print("\n" + "="*80)
print("ANÁLISIS Y AGREGACIONES")
print("="*80)

# Salario promedio por ciudad
print("\n💰 SALARIO PROMEDIO POR CIUDAD:")
df.groupBy("ciudad").avg("salario").show()

# Estadísticas completas por ciudad
print("\n📊 ESTADÍSTICAS COMPLETAS POR CIUDAD:")
city_stats = df.groupBy("ciudad").agg(
    count("*").alias("num_empleados"),
    avg("salario").alias("salario_promedio"),
    avg("edad").alias("edad_promedia"),
    spark_max("salario").alias("salario_maximo")
).orderBy(col("salario_promedio").desc())

city_stats.show()

# Contar empleados por categoría de salario
print("\n📈 DISTRIBUCIÓN POR CATEGORÍA DE SALARIO:")
df_with_category.groupBy("categoria_salario").agg(
    count("*").alias("cantidad"),
    avg("salario").alias("salario_promedio")
).orderBy("categoria_salario").show()

# Análisis por rangos de edad
print("\n👥 ANÁLISIS POR RANGOS DE EDAD:")
df_age_ranges = df.withColumn(
    "rango_edad",
    when(col("edad") < 30, "20-29")
    .when((col("edad") >= 30) & (col("edad") < 40), "30-39")
    .otherwise("40+")
)

df_age_ranges.groupBy("rango_edad").agg(
    count("*").alias("cantidad"),
    avg("salario").alias("salario_promedio"),
    avg("edad").alias("edad_promedia")
).orderBy("rango_edad").show()

# Resumen general
print("\n📊 RESUMEN GENERAL:")
summary = df.agg(
    count("*").alias("total_empleados"),
    avg("edad").alias("edad_promedio"),
    avg("salario").alias("salario_promedio"),
    spark_max("salario").alias("salario_maximo"),
    spark_sum("salario").alias("masa_salarial_total")
)
summary.show()

# ----------------------------------------------------------------------------
# PASO 4.4: GUARDAR RESULTADOS EN HDFS
# ----------------------------------------------------------------------------

print("\n" + "="*80)
print("PASO 4.4: GUARDAR RESULTADOS EN HDFS")
print("="*80)

# Guardar datos filtrados en formato CSV
print("\n💾 Guardando datos filtrados en CSV...")
filtered_df.write.mode("overwrite").option("header", "true").csv(
    "hdfs:///user/data/output_filtered"
)
print("✅ Datos filtrados guardados en: hdfs:///user/data/output_filtered")

# Guardar datos con categorías en formato Parquet
print("\n💾 Guardando datos con categorías en Parquet...")
df_with_category.write.mode("overwrite").parquet(
    "hdfs:///user/data/output_parquet"
)
print("✅ Datos guardados en: hdfs:///user/data/output_parquet")

# Guardar estadísticas por ciudad
print("\n💾 Guardando estadísticas por ciudad...")
city_stats.write.mode("overwrite").option("header", "true").csv(
    "hdfs:///user/data/city_statistics"
)
print("✅ Estadísticas guardadas en: hdfs:///user/data/city_statistics")

print("\n🎉 ¡Todos los datos guardados exitosamente en HDFS!")

# ----------------------------------------------------------------------------
# VERIFICAR ARCHIVOS GUARDADOS
# ----------------------------------------------------------------------------

print("\n" + "="*80)
print("VERIFICAR ARCHIVOS GUARDADOS EN HDFS")
print("="*80)
print("\nEjecutar en terminal SSH:")
print("hdfs dfs -ls /user/data/")
print("hdfs dfs -ls /user/data/output_filtered/")
print("hdfs dfs -ls /user/data/output_parquet/")
print("hdfs dfs -cat /user/data/output_filtered/part-00000* | head -20")

# ----------------------------------------------------------------------------
# LEER DATOS GUARDADOS
# ----------------------------------------------------------------------------

print("\n" + "="*80)
print("LEER DATOS GUARDADOS DESDE HDFS")
print("="*80)

# Leer datos filtrados en CSV
print("\n📂 Leyendo datos filtrados (CSV):")
df_loaded_csv = spark.read.csv(
    "hdfs:///user/data/output_filtered",
    header=True,
    inferSchema=True
)
df_loaded_csv.show(5)

# Leer datos en formato Parquet
print("\n📂 Leyendo datos desde Parquet:")
df_loaded_parquet = spark.read.parquet("hdfs:///user/data/output_parquet")
df_loaded_parquet.show(5)

# Leer estadísticas
print("\n📂 Leyendo estadísticas por ciudad:")
df_stats = spark.read.csv(
    "hdfs:///user/data/city_statistics",
    header=True,
    inferSchema=True
)
df_stats.show()

print("\n✅ ¡Lectura de datos verificada correctamente!")

# ============================================================================
# PARTE 3: CIERRE Y DISCUSIÓN
# ============================================================================

print("\n" + "="*80)
print("PARTE 3: CIERRE Y DISCUSIÓN")
print("="*80)

cierre_discusion = """

╔════════════════════════════════════════════════════════════════════════════╗
║                     CIERRE Y DISCUSIÓN - 30 MINUTOS                        ║
╚════════════════════════════════════════════════════════════════════════════╝

1. REPASO DE ACTIVIDADES REALIZADAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Actividades completadas:
   • Configuración de clúster EMR con HDFS
   • Conexión SSH al nodo maestro
   • Creación de directorios en HDFS
   • Carga de archivos locales a HDFS
   • Lectura de datos con PySpark desde HDFS
   • Procesamiento y transformación de datos
   • Análisis y agregaciones
   • Escritura de resultados en múltiples formatos
   • Verificación de datos guardados


2. DIFICULTADES ENCONTRADAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 DIFICULTADES TÉCNICAS COMUNES:

a) Conexión SSH al nodo maestro:
   Problema: Errores con claves SSH (.pem) y permisos
   Solución: Usar AWS CloudShell como alternativa
   Comando CloudShell: 
   aws emr ssh --cluster-id j-XXXXXXXXXXXXX --key-pair-file ~/key.pem

b) Sintaxis de comandos HDFS:
   Problema: Confusión entre comandos Linux y HDFS
   Recordar: Siempre usar prefijo "hdfs dfs -" para operaciones en HDFS
   Ejemplo: hdfs dfs -ls (no solo "ls")

c) Rutas en HDFS:
   Problema: No distinguir rutas locales de rutas HDFS
   Local: /home/hadoop/archivo.csv
   HDFS: hdfs:///user/data/archivo.csv

d) Tiempo de inicio del clúster:
   Problema: Impaciencia durante los 10-15 minutos de arranque
   Tip: Utilizar este tiempo para revisar teoría o preparar archivos

e) Gestión de recursos:
   Problema: Nodos pequeños sin memoria suficiente
   Solución: Usar tipos de instancia apropiados (m5.xlarge recomendado)

🔴 DIFICULTADES CONCEPTUALES:

a) Distribución de bloques:
   • Entender cómo un archivo se divide en bloques de 128MB
   • Comprender que cada bloque se replica en 3 nodos diferentes
   • Visualizar cómo se distribuye la información físicamente

b) Almacenamiento local vs distribuido:
   • Local: Todo en un disco, si falla se pierde todo
   • Distribuido: Datos replicados, tolerancia a fallos

c) Replicación de datos:
   • Por qué HDFS replica 3 veces (consume 3x espacio)
   • Trade-off: Espacio vs Disponibilidad vs Rendimiento


3. ¿CÓMO HDFS Y PYSPARK AYUDAN EN EL PROCESAMIENTO DISTRIBUIDO?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 HDFS PROPORCIONA:

a) Almacenamiento Escalable:
   • Datos divididos en bloques de 128MB
   • Distribución entre múltiples nodos
   • Capacidad: Terabytes → Petabytes
   
   Ejemplo: 1TB de datos = 8,000 bloques distribuidos en el clúster

b) Tolerancia a Fallos:
   • 3 réplicas por bloque por defecto
   • Si falla un nodo, datos disponibles en otros 2
   • NameNode detecta fallos y replica automáticamente
   
   Ejemplo: En clúster de 100 nodos, pueden fallar 66 nodos 
           y aún así los datos están disponibles

c) Localidad de Datos:
   • Procesamiento donde están los datos
   • Reduce transferencia de red
   • "Mover código a datos" vs "Mover datos a código"
   
   Impacto: Reducción de latencia del 90% en operaciones masivas

🟢 PYSPARK PROPORCIONA:

a) Procesamiento Paralelo:
   • Divide trabajo automáticamente entre nodos
   • Procesamiento simultáneo en múltiples máquinas
   
   Ejemplo: 10 nodos → 10x más rápido que 1 máquina
           Análisis que tarda 10 horas → 1 hora

b) Lazy Evaluation (Evaluación Perezosa):
   • Spark construye un plan de ejecución óptimo
   • No ejecuta hasta que es necesario
   • Optimiza operaciones combinadas
   
   Beneficio: Reducción hasta 50% en operaciones redundantes

c) Abstracción de Complejidad:
   • Código como si fuera una sola máquina
   • Spark maneja la distribución automáticamente
   • APIs de alto nivel (DataFrames, SQL)
   
   Ventaja: Productividad del desarrollador aumenta 3-5x

🟢 EJEMPLO PRÁCTICO DEL BENEFICIO COMBINADO:

Escenario: Analizar 1TB de logs de servidores web

❌ SIN DISTRIBUCIÓN (1 servidor potente):
   • Tiempo: ~10 horas
   • Si falla: Perder todo el trabajo
   • Costo: Servidor de alto rendimiento caro

✅ CON HDFS + PYSPARK (10 nodos medianos):
   • Tiempo: ~1 hora (10x más rápido)
   • Si falla 1-2 nodos: Trabajo continúa
   • Costo: Nodos económicos, escalable bajo demanda


4. CASOS PRÁCTICOS EN LA INDUSTRIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💼 CASO 1: ANÁLISIS DE LOGS (Netflix, Amazon)
   Problema: Procesar 50TB de logs diarios
   Solución: HDFS almacena logs, Spark analiza patrones
   Resultado: Detectar errores en minutos vs horas
   Beneficio: Mejor experiencia de usuario, menos downtime

💼 CASO 2: DETECCIÓN DE FRAUDE (Bancos, PayPal)
   Problema: Analizar 100M de transacciones/día en tiempo real
   Solución: Spark Streaming + HDFS para histórico
   Resultado: Detección de fraude en segundos
   Beneficio: Prevención de pérdidas millonarias

💼 CASO 3: IoT Y SMART CITIES (Empresas municipales)
   Problema: 10,000 sensores generando datos cada segundo
   Solución: HDFS para series temporales, Spark para análisis
   Resultado: Optimización de tráfico y energía
   Beneficio: Ahorro 20-30% en costos operativos

💼 CASO 4: RECOMENDACIONES (Spotify, YouTube, Netflix)
   Problema: Procesar billones de interacciones usuario-contenido
   Solución: HDFS guarda histórico, Spark entrena modelos ML
   Resultado: Recomendaciones personalizadas precisas
   Beneficio: +40% engagement, +25% retención de usuarios

💼 CASO 5: ANÁLISIS SATELITAL (NASA, Agricultura)
   Problema: Procesar terabytes de imágenes satelitales
   Solución: HDFS almacena imágenes, Spark procesa en paralelo
   Resultado: Detección de cambios climáticos y cultivos
   Beneficio: Predicciones agrícolas más precisas

💼 CASO 6: REDES SOCIALES (Meta, Twitter)
   Problema: Procesar millones de posts/segundo
   Solución: HDFS para grafo social, Spark para análisis
   Resultado: Detección de tendencias y moderación automática
   Beneficio: Plataforma más segura y relevante


5. COMPARACIÓN: CON Y SIN TECNOLOGÍAS BIG DATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────────────────┐
│ MÉTRICA          │ SIN BIG DATA      │ CON HDFS + PYSPARK              │
├─────────────────────────────────────────────────────────────────────────┤
│ Tiempo proceso   │ 10 horas          │ 1 hora (10x más rápido)         │
│ Escalabilidad    │ Vertical (cara)   │ Horizontal (económica)          │
│ Tolerancia fallo │ Ninguna           │ Alta (réplicas)                 │
│ Capacidad        │ Limitada (1 disco)│ Petabytes                       │
│ Costo            │ $10,000/mes       │ $2,000/mes (bajo demanda)       │
│ Flexibilidad     │ Baja              │ Alta (añadir nodos)             │
└─────────────────────────────────────────────────────────────────────────┘


6. PREGUNTAS PARA REFLEXIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ ¿En qué situaciones NO usarías HDFS?
   → Datos pequeños (< 1GB)
   → Aplicaciones transaccionales (OLTP)
   → Necesidad de latencia ultra-baja (< 10ms)

❓ ¿Qué pasaría si el NameNode falla?
   → Sin HA: Clúster inoperativo
   → Con HA: Secondary NameNode toma el control

❓ ¿Cómo elegir el número de réplicas?
   → 3 réplicas: Balance estándar
   → 2 réplicas: Menos redundancia, más espacio
   → 4+ réplicas: Datos críticos, más seguridad

❓ ¿Cuándo usar Parquet vs CSV?
   → Parquet: Análisis frecuentes, queries selectivas
   → CSV: Intercambio de datos, compatibilidad


7. RECURSOS PARA CONTINUAR APRENDIENDO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 Documentación Oficial:
   • Apache Spark: https://spark.apache.org/docs/latest/
   • AWS EMR: https://docs.aws.amazon.com/emr/
   • HDFS: https://hadoop.apache.org/docs/

📖 Libros Recomendados:
   • "Learning Spark" (O'Reilly)
   • "Hadoop: The Definitive Guide" (O'Reilly)
   • "High Performance Spark" (O'Reilly)

🎓 Cursos Online:
   • Coursera: Big Data Specialization
   • DataCamp: PySpark courses
   • Udemy: Spark and Hadoop Developer

💻 Práctica con Datos Reales:
   • Kaggle: Big Data competitions
   • AWS Open Data: Datasets públicos
   • Google BigQuery: Public datasets


8. PRÓXIMOS PASOS SUGERIDOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Nivel Intermedio:
   • Integrar HDFS con Apache Hive para consultas SQL
   • Usar Spark MLlib para machine learning distribuido
   • Implementar particionamiento de datos en HDFS

🎯 Nivel Avanzado:
   • Configurar clúster en Alta Disponibilidad (HA)
   • Optimizar performance con caché y persistencia
   • Implementar Spark Streaming para datos en tiempo real
   • Integrar con Kafka para pipelines de datos

╔════════════════════════════════════════════════════════════════════════════╗
║                         ¡PRÁCTICA COMPLETADA!                              ║
║                                                                            ║
║  Has aprendido los fundamentos de HDFS y PySpark en un entorno real.     ║
║  Estos conocimientos son la base para trabajar con Big Data.              ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

print(cierre_discusion)

# ============================================================================
# LIMPIEZA Y CIERRE
# ============================================================================

print("\n" + "="*80)
print("LIMPIEZA Y CIERRE")
print("="*80)

limpieza = """
COMANDOS DE LIMPIEZA EN TERMINAL SSH:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Ver todos los archivos creados
hdfs dfs -ls -R /user/data/

# Eliminar archivos de salida
hdfs dfs -rm -r /user/data/output_*

# Eliminar estadísticas
hdfs dfs -rm -r /user/data/city_statistics

# Limpiar todo el directorio (CUIDADO)
hdfs dfs -rm -r /user/data/*

# Verificar espacio liberado
hdfs dfs -du -h /user/

# Verificar estado del sistema
hdfs dfsadmin -report


PARA DETENER EL CLÚSTER EMR (Importante para no gastar créditos):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. En la consola AWS EMR
2. Seleccionar el clúster
3. Clic en "Terminate"
4. Confirmar terminación

⚠️  NOTA: Terminar el clúster eliminará todos los datos en HDFS
    Si necesitas conservar datos, guárdalos en S3 antes de terminar
"""

print(limpieza)

# Detener sesión de Spark
print("\n📌 Para detener la sesión de Spark, ejecuta:")
print("spark.stop()")

print("\n" + "="*80)
print("✅ ¡PRÁCTICA COMPLETADA EXITOSAMENTE!")
print("="*80)
print("""
Conceptos Aprendidos:
✓ Arquitectura y funcionamiento de HDFS
✓ Comandos básicos para interactuar con HDFS
✓ Lectura y escritura de datos con PySpark
✓ Transformaciones y filtros de datos distribuidos
✓ Agregaciones y análisis estadístico
✓ Diferentes formatos de almacenamiento (CSV, Parquet)
✓ Beneficios del procesamiento distribuido
✓ Casos de uso reales en la industria

¡Felicitaciones! Ahora tienes las bases para trabajar con Big Data.
""")
