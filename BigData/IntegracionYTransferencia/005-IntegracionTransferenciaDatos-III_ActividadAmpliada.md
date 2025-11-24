
---

# 🧪 **2. Actividad Detallada (Versión ampliada)**

(diseñada para UD2 o para el compañero de BD aplicado)

Te la dejo en formato didáctico, paso a paso y autónoma.
Lista para entregar al alumnado o integrarla en el aula virtual.

---

# 🎓 **Actividad: Construcción de un Pipeline Moderno de Ingesta e Integración de Datos (Airbyte + CDC + Kafka + Python)**

## ✔️ Objetivo general

Construir un pipeline real completo utilizando:

* **PostgreSQL Cloud** (Neon)
* **Airbyte Cloud** (ingesta batch/incremental)
* **Confluent Cloud (Kafka)** (CDC)
* **Python (Google Colab)** (consumer streaming)

El alumnado experimentará **dos enfoques modernos**:

* *Batch/Incremental ELT* (Airbyte)
* *CDC Streaming* (Debezium-like con Confluent)

El ejercicio no requiere instalación local de nada.

---

## 🧩 **1. Crear la base de datos en Neon (PostgreSQL Cloud)**

1. Entrar en [https://neon.tech](https://neon.tech)
2. Crear un proyecto nuevo
3. Anotar los datos:

   * HOST
   * USER
   * PASSWORD
   * DATABASE
   * PORT
4. En el SQL Editor crear la tabla:

```sql
CREATE TABLE clientes (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100),
  email VARCHAR(100),
  actualizado TIMESTAMP DEFAULT NOW()
);
```

5. Insertar datos:

```sql
INSERT INTO clientes(nombre, email)
VALUES ('Ana', 'ana@example.com'),
       ('Luis', 'luis@example.com');
```

---

## 🟦 **2. Crear el CDC con Confluent Cloud (Kafka gestionado)**

1. Entrar en [https://confluent.cloud](https://confluent.cloud)
2. Crear cuenta gratuita
3. Crear cluster “Basic”
4. Ir a **Connectors → PostgreSQL CDC Source**
5. Configurar:

   * Host = host de Neon
   * User/password
   * Database
   * Table inclusion: `clientes`
6. Seleccionar topic destino:

   ```
   clientes_cdc
   ```

Una vez activado, cualquier cambio en la tabla `clientes` aparecerá como evento CDC en Kafka.

---

## 🟨 **3. Ingesta batch/incremental con Airbyte Cloud**

1. Entrar en [https://cloud.airbyte.com](https://cloud.airbyte.com)
2. Crear cuenta gratuita
3. Crear **Source**:

   * Tipo: PostgreSQL
   * Host/DB/User/Password = datos de Neon
4. Crear **Destination**:

   * Tipo: *File (JSON o Parquet)*
   * Carpeta interna: `airbyte_output/`
5. Crear **Connection**:

   * Sync mode: *Incremental*
   * Cursor: `actualizado`
   * Primary key: `id`
6. Ejecutar sincronización manual

El resultado será un conjunto de ficheros Parquet/JSON exportados.

---

## 🐍 **4. Crear el consumidor en Google Colab**

1. Abrir [https://colab.research.google.com](https://colab.research.google.com)
2. Instalar librería:

```python
!pip install confluent-kafka
```

3. Añadir código del consumidor:

```python
from confluent_kafka import Consumer
import json

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

4. Ejecutar el notebook
5. Volver a Neon y modificar datos:

```sql
UPDATE clientes 
SET nombre = 'Ana Gómez' 
WHERE id = 1;
```

En Colab aparece inmediatamente el evento CDC.

---

## 📄 **5. Documentación a entregar**

El alumnado debe entregar:

* Diagrama del pipeline (simple o con Mermaid)
* Capturas de:

  * Airbyte Source
  * Airbyte Destination
  * Airbyte Sync
  * Conector CDC en Confluent
  * Topic con mensajes
  * Colab mostrando eventos
* Script del consumidor explicando cada línea
* Informe técnico (1–2 páginas):

  * Qué herramientas han usado
  * Qué problema resuelve cada una
  * Ventajas/inconvenientes
  * Qué podrían añadir o mejorar

---

## 🎯 **6. Resultado esperado**

Al final, los alumnos habrán construido un pipeline que:

* lee datos batch/incrementales desde PostgreSQL → Airbyte
* captura cambios CDC PostgreSQL → Confluent Kafka
* los visualiza en tiempo real → Python (Colab)

---

# 👍 **Todo listo.**


