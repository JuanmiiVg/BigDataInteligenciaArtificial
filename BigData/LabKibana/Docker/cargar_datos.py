#!/usr/bin/env python3
"""
Script para cargar datos de ejemplo en Elasticsearch
"""

import requests
import json
from datetime import datetime, timedelta
import random

ELASTICSEARCH_URL = "http://localhost:9200"
INDEX_NAME = "ventas"

# Datos de ejemplo
ciudades = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"]
productos = ["Laptop", "Smartphone", "Tablet", "Monitor", "Teclado", "Ratón", "Auriculares"]
categorias = ["Electrónica", "Informática", "Accesorios"]
estados = ["Completado", "Pendiente", "Cancelado"]

def crear_indice():
    """Crea el índice en Elasticsearch"""
    url = f"{ELASTICSEARCH_URL}/{INDEX_NAME}"
    
    mapping = {
        "mappings": {
            "properties": {
                "fecha": {"type": "date"},
                "ciudad": {"type": "keyword"},
                "producto": {"type": "keyword"},
                "categoria": {"type": "keyword"},
                "cantidad": {"type": "integer"},
                "precio": {"type": "float"},
                "total": {"type": "float"},
                "estado": {"type": "keyword"},
                "vendedor": {"type": "keyword"}
            }
        }
    }
    
    # Eliminar índice si existe
    requests.delete(url)
    
    # Crear nuevo índice
    response = requests.put(url, json=mapping)
    print(f"Índice creado: {response.status_code}")
    return response.status_code == 200

def generar_ventas(num_ventas=500):
    """Genera ventas de ejemplo"""
    ventas = []
    fecha_base = datetime.now() - timedelta(days=90)
    
    for i in range(num_ventas):
        fecha = fecha_base + timedelta(
            days=random.randint(0, 90),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        producto = random.choice(productos)
        cantidad = random.randint(1, 10)
        precio = random.uniform(10, 1500)
        
        # Asignar categoría según producto
        if producto in ["Laptop", "Smartphone", "Tablet"]:
            categoria = "Electrónica"
        elif producto in ["Monitor", "Teclado", "Ratón"]:
            categoria = "Informática"
        else:
            categoria = "Accesorios"
        
        venta = {
            "fecha": fecha.isoformat(),
            "ciudad": random.choice(ciudades),
            "producto": producto,
            "categoria": categoria,
            "cantidad": cantidad,
            "precio": round(precio, 2),
            "total": round(precio * cantidad, 2),
            "estado": random.choice(estados),
            "vendedor": f"Vendedor_{random.randint(1, 20)}"
        }
        ventas.append(venta)
    
    return ventas

def cargar_datos(ventas):
    """Carga los datos en Elasticsearch usando Bulk API"""
    url = f"{ELASTICSEARCH_URL}/_bulk"
    
    bulk_data = []
    for venta in ventas:
        # Acción de índice
        bulk_data.append(json.dumps({"index": {"_index": INDEX_NAME}}))
        # Documento
        bulk_data.append(json.dumps(venta))
    
    bulk_body = "\n".join(bulk_data) + "\n"
    
    headers = {"Content-Type": "application/x-ndjson"}
    response = requests.post(url, data=bulk_body, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        errores = [item for item in result['items'] if 'error' in item.get('index', {})]
        if errores:
            print(f"⚠️  Se encontraron {len(errores)} errores")
        else:
            print(f"✅ {len(ventas)} documentos cargados correctamente")
    else:
        print(f"❌ Error al cargar datos: {response.status_code}")
        print(response.text)
    
    return response.status_code == 200

def verificar_datos():
    """Verifica cuántos documentos se han cargado"""
    url = f"{ELASTICSEARCH_URL}/{INDEX_NAME}/_count"
    response = requests.get(url)
    
    if response.status_code == 200:
        count = response.json()['count']
        print(f"\n📊 Total de documentos en el índice '{INDEX_NAME}': {count}")
    else:
        print(f"❌ Error al verificar datos: {response.status_code}")

def main():
    print("🚀 Cargando datos de ejemplo en Elasticsearch...\n")
    
    # Crear índice
    if not crear_indice():
        print("❌ Error al crear el índice")
        return
    
    # Generar y cargar ventas
    print("📦 Generando datos de ventas...")
    ventas = generar_ventas(500)
    
    print(f"⬆️  Cargando {len(ventas)} ventas...")
    if cargar_datos(ventas):
        verificar_datos()
        print("\n✅ ¡Proceso completado con éxito!")
        print(f"\n👉 Ahora puedes acceder a Kibana: http://localhost:5601")
    else:
        print("\n❌ Hubo un problema al cargar los datos")

if __name__ == "__main__":
    main()
