"""
Script rápido para verificar datos en MongoDB y PostgreSQL
"""
import sys
import os
import psycopg2
from pymongo import MongoClient

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config.settings import POSTGRES_URI, MONGO_URI, MONGO_DB

def check_mongodb():
    """Verifica datos en MongoDB"""
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        
        print("🟢 MongoDB conectado")
        
        # Colecciones
        colecciones = db.list_collection_names()
        print(f"  Colecciones: {colecciones}")
        
        # Consumos diarios
        if "consumos_diarios" in colecciones:
            count = db["consumos_diarios"].count_documents({})
            print(f"  📊 consumos_diarios: {count} registros")
        
        # Consumos mensuales
        if "consumos_mensuales" in colecciones:
            count = db["consumos_mensuales"].count_documents({})
            print(f"  📅 consumos_mensuales: {count} registros")
            
            # Mostrar ejemplos
            ejemplos = list(db["consumos_mensuales"].find().limit(3))
            for doc in ejemplos:
                print(f"     - {doc.get('propietario_id')} | {doc.get('mes_str')}")
        
        # Anomalías
        if "anomalias_detectadas" in colecciones:
            count = db["anomalias_detectadas"].count_documents({})
            print(f"  🚨 anomalias_detectadas: {count} registros")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error MongoDB: {e}")

def check_postgresql():
    """Verifica datos en PostgreSQL"""
    try:
        conn = psycopg2.connect(POSTGRES_URI)
        cursor = conn.cursor()
        
        print("\n🟢 PostgreSQL conectado")
        
        # Tablas
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tablas = [row[0] for row in cursor.fetchall()]
        print(f"  Tablas: {tablas}")
        
        # Consumos diarios
        if "consumos_diarios" in tablas:
            cursor.execute("SELECT COUNT(*) FROM consumos_diarios")
            count = cursor.fetchone()[0]
            print(f"  📊 consumos_diarios: {count} registros")
            
            # Mostrar ejemplo
            cursor.execute("""
                SELECT propietario_id, fecha, COUNT(*) as registros 
                FROM consumos_diarios 
                GROUP BY propietario_id, fecha 
                LIMIT 3
            """)
            for row in cursor.fetchall():
                print(f"     - {row[0]} | {row[1]} | {row[2]} registros")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error PostgreSQL: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 Verificación de Datos - ConsumoDeDatos")
    print("=" * 60)
    
    check_mongodb()
    check_postgresql()
    
    print("\n" + "=" * 60)
