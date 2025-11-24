# Herramientas modernas de integración y transferencia de datos: Airbyte, Debezium y Kafka

------------------------------------------------------------------------

# Ampliación teórica \*\*

# 📘 **1. Introudcción a MinIO**

**MinIO** es una alternativa *open-source* y ligera al servicio Amazon S3.

Implementa la API oficial de S3, por lo que herramientas como Airbyte, Spark, Kafka Connect o Python pueden trabajar con MinIO exactamente igual que si fuera AWS S3.

### ¿Para qué lo usamos en Big Data?

-   Para simular un **data lake** (zona RAW / STAGED / CURATED).
-   Para almacenar **ficheros Parquet**, **CSV**, **JSON**, logs…
-   Para probar pipelines sin necesidad de usar AWS.

### ¿Por qué lo usamos en clase?

-   No requiere cuenta cloud.
-   Es muy ligero (solo un contenedor Docker).
-   Compatible con los conectores modernos.

------------------------------------------------------------------------

# 📘 **2. Introducción de Zookeeper**

Tradicionalmente, Kafka dependía de un sistema externo llamado **Zookeeper**, cuyo cometido es:

-   Mantener información de estado de los brokers Kafka
-   Coordinar controladores en el cluster
-   Elegir líderes para particiones
-   Almacenar metadatos de configuración

**HOY:** Kafka moderno incluye un modo llamado *KIP-500* que elimina Zookeeper, pero muchas distribuciones de Debezium y Kafka Connect **todavía usan la arquitectura clásica**.

### ¿Por qué aparece en nuestra práctica?

Porque Debezium + Kafka Connect dependen de la arquitectura tradicional de Kafka, donde Zookeeper es obligatorio. Es importante conocerlo al menos a nivel conceptual.

------------------------------------------------------------------------

# 📘 **3. PRÁCTICA A (LOCAL CON DOCKER) — COMPLETA**

Perfecta para equipos con CPU/RAM suficientes.

## 🎯 Objetivo de la práctica

Crear un entorno Big Data moderno con:

-   **PostgreSQL** → base de datos origen
-   **Airbyte** → ingesta batch/incremental hacia MinIO
-   **MinIO** → data lake (simulación S3)
-   **Kafka + Zookeeper** → plataforma de streaming
-   **Debezium** → CDC desde PostgreSQL hacia Kafka
-   **Python script** → consumer Kafka para ver los cambios de la BD en tiempo real

------------------------------------------------------------------------

# 🐳 **3.1. Docker Compose completo (listo para copiar y pegar)**

Guárdalo como:

```         
docker-compose.yml
```

``` yaml
version: "3.8"

services:

  # -----------------------
  # 1. PostgreSQL
  # -----------------------
  postgres:
    image: debezium/example-postgres:1.9
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=empresa
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  # -----------------------
  # 2. Zookeeper
  # -----------------------
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    ports:
      - "2181:2181"

  # -----------------------
  # 3. Kafka broker
  # -----------------------
  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  # -----------------------
  # 4. Debezium connect
  # -----------------------
  connect:
    image: debezium/connect:1.9
    depends_on:
      - kafka
      - postgres
    ports:
      - "8083:8083"
    environment:
      BOOTSTRAP_SERVERS: kafka:9092
      GROUP_ID: 1
      CONFIG_STORAGE_TOPIC: debezium_config
      OFFSET_STORAGE_TOPIC: debezium_offsets
      STATUS_STORAGE_TOPIC: debezium_status
      KEY_CONVERTER_SCHEMAS_ENABLE: "false"
      VALUE_CONVERTER_SCHEMAS_ENABLE: "false"

  # -----------------------
  # 5. MinIO (S3 simulado)
  # -----------------------
  minio:
    image: minio/minio
    environment:
      MINIO_ROOT_USER: minio
      MINIO_ROOT_PASSWORD: minio123
    command: server /data
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data

  # -----------------------
  # 6. Airbyte
  # -----------------------
  airbyte-webapp:
    image: airbyte/webapp:0.40.22
    ports:
      - "8000:8000"
    depends_on:
      - airbyte-server

  airbyte-server:
    image: airbyte/server:0.40.22
    ports:
      - "8001:8001"
    environment:
      - AIRBYTE_ROLE=server
    volumes:
      - airbyte_data:/data

volumes:
  pgdata:
  minio_data:
  airbyte_data:
```

------------------------------------------------------------------------

# 🚀 **3.2. Cómo lanzar el entorno**

Desde el directorio donde guardaste el `docker-compose.yml`:

```         
docker compose up -d
```

Comprobar que todo está funcionando:

```         
docker compose ps
```

Accesos:

| Servicio       | URL                     |
|----------------|-------------------------|
| Airbyte        | <http://localhost:8000> |
| MinIO Console  | <http://localhost:9001> |
| Kafka (broker) | localhost:9092          |
| Debezium API   | <http://localhost:8083> |
| PostgreSQL     | localhost:5432          |

------------------------------------------------------------------------

# 🛢 **3.3. Configuración de PostgreSQL**

Conectar:

```         
psql -h localhost -U postgres -d empresa
```

Crear tabla de ejemplo:

``` sql
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    email VARCHAR(100),
    actualizado TIMESTAMP DEFAULT NOW()
);
```

Insertar algunas filas:

``` sql
INSERT INTO clientes(nombre, email) 
VALUES ('Ana', 'ana@example.com'), ('Luis', 'luis@example.com');
```

------------------------------------------------------------------------

# 🔄 **3.4. Configurar Airbyte — PostgreSQL → MinIO**

### ✨ Pasos

1.  Abrir navegador → <http://localhost:8000>

2.  Crear **Source**

    -   Tipo: PostgreSQL
    -   Host: `postgres`
    -   DB: `empresa`
    -   User: `postgres`
    -   Pass: `postgres`

3.  Crear **Destination**

    -   Tipo: S3 / MinIO
    -   Endpoint: `http://minio:9000`
    -   Access key: `minio`
    -   Secret key: `minio123`
    -   Bucket: `datalake` (créalo desde la consola de MinIO)
    -   Output format: Parquet

4.  Crear **Connection**

    -   Source: PostgreSQL
    -   Destination: MinIO
    -   Sync mode: Incremental
    -   Cursor: `actualizado`
    -   Primary key: `id`

5.  Ejecutar sincronización manual.

Verás los Parquet en MinIO → Bucket `datalake` → carpeta `raw/`.

------------------------------------------------------------------------

# 🔁 **3.5. Configurar Debezium — PostgreSQL → Kafka**

Enviar petición para crear el conector:

```         
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
  "name": "clientes-cdc",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "postgres",
    "database.password": "postgres",
    "database.dbname": "empresa",
    "topic.prefix": "cdc",
    "slot.name": "debezium_slot",
    "plugin.name": "pgoutput"
  }
}'
```

Debezium creará topics como:

```         
cdc.public.clientes
```

------------------------------------------------------------------------

# 🐍 **3.6. Script Python consumidor Kafka (explicado)**

Guardar como:

```         
consumer.py
```

``` python
from kafka import KafkaConsumer
import json

# 1. Creamos el consumer
consumer = KafkaConsumer(
    'cdc.public.clientes',           # topic al que nos conectamos
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',    # recibir todos los mensajes
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Escuchando cambios en la tabla clientes...\n")

# 2. Bucle infinito que espera y procesa mensajes
for msg in consumer:
    evento = msg.value
    print("Evento CDC recibido:")
    print(json.dumps(evento, indent=2))
```

### ¿Qué hace cada import?

-   `KafkaConsumer` → permite leer mensajes del topic
-   `json` → para formatear los mensajes Debezium

### ¿Cómo ejecutarlo?

```         
pip install kafka-python
python consumer.py
```

En otra terminal, modifica datos en PostgreSQL:

``` sql
UPDATE clientes SET nombre='Ana Maria' WHERE id=1;
```

El consumer mostrará el evento.

------------------------------------------------------------------------

Perfecto, José Manuel. Vamos con **FASE 2 — Versión Cloud de la práctica** para que TODOS los alumnos puedan hacerla **aunque no tengan potencia suficiente en sus equipos**.

Esta versión cloud es:

-   100% funcional
-   100% gratuita (usando *free tiers* reales)
-   100% ejecutable desde navegador y/o Google Colab
-   No requiere Docker local ni instalación de nada en el equipo del alumno

------------------------------------------------------------------------

# 🌐 **FASE 2 — Práctica en la nube (sin instalaciones locales)**

*Airbyte Cloud + Kafka gestionado + PostgreSQL Cloud + script desde Colab*

------------------------------------------------------------------------

# 🧩 **1. Arquitectura Cloud propuesta**

```         
┌────────────────────────┐
│  Airbyte Cloud          │
│  (Source: PostgreSQL    │
│   Destination: S3-like) │
└──────────────▲─────────┘
               │ ELT batch/incremental
               │
┌──────────────┴─────────┐
│ PostgreSQL Cloud (Neon)│
│ (Base de datos origen) │
└──────────────▲─────────┘
               │ CDC events
               │
┌──────────────┴────────────┐
│ Confluent Cloud (Kafka)    │
│ (Topic: clientes_cdc)      │
└──────────────▲────────────┘
               │ Consumer
               │
┌──────────────┴────────────┐
│ Google Colab / Python      │
│ (Consumer en tiempo real)  │
└────────────────────────────┘
```

------------------------------------------------------------------------

# ⭐ **2. Servicios gratuitos que usaremos**

### 🟦 **PostgreSQL Cloud (Neon Tech)**

-   100% gratis, sin tarjeta
-   Alta disponibilidad
-   Permite activar el *logical replication* sin complicaciones
-   Web UI muy clara para los alumnos

👉 <https://neon.tech>

------------------------------------------------------------------------

### 🟧 **Kafka gestionado (Confluent Cloud)**

-   1 cluster gratuito (Kafka + Schema Registry)
-   Perfecto para Debezium y prácticas de streaming
-   Panel gráfico excelente para mostrar temas y mensajes

👉 <https://confluent.cloud>

------------------------------------------------------------------------

### 🟨 **Airbyte Cloud Free Tier**

-   No requiere instalación
-   Permite crear Sources y Destinations desde navegador

👉 <https://cloud.airbyte.com>

------------------------------------------------------------------------

### 🟩 **Google Colab**

-   Ejecuta Python desde navegador
-   Los alumnos pueden hacer el consumer Kafka sin instalar nada

👉 <https://colab.research.google.com>

------------------------------------------------------------------------

# 🔎 **3. Paso a paso detallado para los alumnos**

------------------------------------------------------------------------

# ☁️ **3.1. Crear PostgreSQL en Neon**

1.  Entrar en <https://neon.tech>

2.  Crear cuenta (Google o GitHub).

3.  Crear proyecto nuevo:

    -   Database: `empresa`
    -   Usuario: `neon_user`
    -   Password: generada automáticamente

4.  Anotar los datos de conexión:

    -   HOST
    -   PORT (normalmente 5432)
    -   USER
    -   PASSWORD
    -   DATABASE NAME

5.  Entrar en **SQL Editor** y crear tabla:

``` sql
CREATE TABLE clientes (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100),
  email VARCHAR(120),
  actualizado TIMESTAMP DEFAULT NOW()
);
```

6.  Insertar datos iniciales:

``` sql
INSERT INTO clientes(nombre, email)
VALUES ('Ana', 'ana@example.com'),
       ('Luis', 'luis@example.com');
```

------------------------------------------------------------------------

# 🔄 **3.2. Configurar Debezium (sin instalar Debezium)**

Como los alumnos no pueden instalar Debezium en cloud, lo sustituimos por:

### ⭐ **Confluent Cloud Connectors → Source PostgreSQL CDC**

Esto es ideal porque:

-   Hace *exactamente* lo que hace Debezium
-   Es totalmente gestionado
-   No consume recursos locales
-   es didácticamente perfecto para RA3

### ✔️ Pasos

1.  Entrar en: <https://confluent.cloud>

2.  Crear cuenta (no necesita tarjeta).

3.  Crear cluster “Basic” (gratuito).

4.  En la barra lateral → **Connectors**.

5.  Elegir: **PostgreSQL CDC Source**.

6.  Introducir credenciales de Neon.

7.  Seleccionar tabla `clientes`.

8.  Elegir topic destino:

    ```         
    clientes_cdc
    ```

### Resultado:

Cualquier INSERT/UPDATE/DELETE en Neon → aparece como mensaje CDC en Kafka.

------------------------------------------------------------------------

# ✨ **3.3. Configurar Airbyte Cloud — PostgreSQL → S3 compatible**

Para simular un Data Lake sin usar MinIO local, usaremos:

### ⭐ **“File Destination” de Airbyte Cloud**

que no requiere credenciales S3.

Pasos:

1.  Entrar en <https://cloud.airbyte.com>

2.  Crear cuenta gratuita

3.  Crear **Source**

    -   Tipo: PostgreSQL
    -   Host: el de Neon
    -   Database: empresa
    -   User/password

4.  Crear **Destination**

    -   Tipo: *Local JSON / Parquet Output* (sin S3)

5.  Crear Connection:

    -   Modo: Incremental
    -   Cursor: `actualizado`
    -   Primary key: `id`

Ejecutar sincronización y ver los archivos generados.

------------------------------------------------------------------------

# 🐍 **3.4. Consumer en Google Colab — Los alumnos ven los eventos en tiempo real**

Abren un cuaderno en Colab y pegan:

``` python
!pip install confluent-kafka
```

``` python
from confluent_kafka import Consumer
import json

# Configurar consumer con las credenciales de Confluent Cloud
conf = {
    'bootstrap.servers': 'CLUSTER_BOOTSTRAP_URL',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'API_KEY',
    'sasl.password': 'API_SECRET',
    'group.id': 'grupo1',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(["clientes_cdc"])

print("Esperando cambios CDC...\n")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Error:", msg.error())
        continue

    evento = json.loads(msg.value().decode("utf-8"))
    print(json.dumps(evento, indent=2))
```

------------------------------------------------------------------------

# 🔔 **3.5. Probar el pipeline completo**

En Neon → ejecutar:

``` sql
UPDATE clientes SET nombre='Ana Gómez' WHERE id=1;
```

En Colab aparecerá:

``` json
{
  "before": {"id": 1, "nombre": "Ana", "email": "ana@example.com"},
  "after": {"id": 1, "nombre": "Ana Gómez", "email": "ana@example.com"},
  "op": "u"
}
```

¡Magia! Y **sin instalar nada local**.

------------------------------------------------------------------------

# 📝4 **RÚBRICA — Actividad: Pipeline moderno de ingesta e integración de datos (Airbyte + CDC + Kafka)**

| Criterio | Indicadores observables | Nivel Excelente (10–9) | Nivel Notable (8–7) | Nivel Adecuado (6–5) | Nivel Insuficiente (\<5) | Peso |
|----|----|----|----|----|----|----|
| **1. Diseño del pipeline** | Diagrama, descripción del flujo, identificación de los componentes | El pipeline está completamente definido, con diagrama claro, etapas explicadas y excelente coherencia técnica | Pipeline definido pero con menor detalle en las interacciones | Pipeline incompleto con varios huecos o explicación justa | No se entiende el flujo o faltan partes esenciales | **20%** |
| **2. Configuración del Source y Destination (Airbyte)** | Source PostgreSQL, destino S3/Parquet, configuración incremental | Configurado correctamente, con capturas, sync incremental funcionando | Configuración correcta pero falta alguna captura o explicación | Configuración solo parcial o poco explicada | No funciona o no se ha configurado | **20%** |
| **3. Configuración CDC (Debezium/Confluent)** | Conector PostgreSQL CDC → Kafka, topic creado | Configuración completa y operativa. Topic CDC leyendo cambios correctamente | Funciona, pero con menos documentación o alguna captura ausente | Configuración incompleta o cambios no llegan a Kafka | No se ha realizado o no funciona | **20%** |
| **4. Script del consumidor Kafka (Python/Colab)** | Lectura de eventos + explicación del código | Script 100% funcional, bien explicado y comentado, eventos leídos y mostrados correctamente | Script funcional con pocos comentarios | Script funcional pero sin comentarios o sin usar correctamente los eventos | Script no funciona | **15%** |
| **5. Calidad del informe técnico** | Claridad, estructura, explicación de problemas y soluciones | Informe claro, organizado y profesional. Se explican problemas y soluciones | Informe claro aunque menos detallado | Informe adecuado pero superficial | Informe incompleto o desordenado | **15%** |
| **6. Reflexión final y valoración de herramientas** | Ventajas/inconvenientes de Airbyte, CDC, Kafka | Excelente reflexión madura y crítica | Buena reflexión pero menos profunda | Reflexión superficial | No hay reflexión | **10%** |

------------------------------------------------------------------------

# 🔢 **Recuento final automático**

Puedes sugerir al alumno calcular:

```         
Nota final = Σ (criterio_nota × peso)
```
