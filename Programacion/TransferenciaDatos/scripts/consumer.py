"""
Consumer Kafka - CDC en tiempo real
Escucha eventos Debezium de PostgreSQL
"""

from kafka import KafkaConsumer
import json
from datetime import datetime

KAFKA_BOOTSTRAP_SERVERS = 'localhost:29092'
TOPICS = [
    'cdc.public.clientes',
    'cdc.public.productos',
    'cdc.public.pedidos'
]

def formatear_evento(evento):
    if not evento:
        return "Evento vacío"

    op_map = {
        'c': '➕ INSERT',
        'u': '✏️ UPDATE',
        'd': '❌ DELETE',
        'r': '📖 SNAPSHOT'
    }

    op = evento.get('op', '?')
    salida = []
    salida.append("=" * 60)
    salida.append(f"🔔 EVENTO CDC - {datetime.now().strftime('%H:%M:%S')}")
    salida.append(f"   Operación: {op_map.get(op, op)}")

    if evento.get('before'):
        salida.append("   📋 BEFORE:")
        for k, v in evento['before'].items():
            salida.append(f"      {k}: {v}")

    if evento.get('after'):
        salida.append("   📋 AFTER:")
        for k, v in evento['after'].items():
            salida.append(f"      {k}: {v}")

    salida.append("=" * 60)
    return "\n".join(salida)

def main():
    consumer = KafkaConsumer(
        *TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        group_id='consumer-practica-cdc',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None
    )

    print("✅ Consumer conectado a Kafka")
    print("👂 Escuchando eventos CDC...\n")

    for msg in consumer:
        print(formatear_evento(msg.value))

if __name__ == "__main__":
    main()
