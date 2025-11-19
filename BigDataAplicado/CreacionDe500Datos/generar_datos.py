import csv
import random
from datetime import datetime, timedelta
from faker import Faker

# Inicializar Faker en español
fake = Faker('es_ES')

# Configuración
NUM_CLIENTES = 500
YEAR = 2022

# Tipos de vivienda (afecta al consumo)
TIPOS_VIVIENDA = [
    {"tipo": "piso_pequeño", "factor": 0.7, "prob": 0.3},      # 30% - 50-80m²
    {"tipo": "piso_mediano", "factor": 1.0, "prob": 0.35},     # 35% - 80-120m²
    {"tipo": "piso_grande", "factor": 1.3, "prob": 0.15},      # 15% - 120-180m²
    {"tipo": "casa_adosada", "factor": 1.5, "prob": 0.15},     # 15% - Casa adosada
    {"tipo": "chalet", "factor": 2.0, "prob": 0.05},           # 5% - Chalet individual
]

# Tipos de instalación solar
TIPOS_INSTALACION = [
    {"tipo": "sin_placas", "potencia": 0, "prob": 0.20},       # 20% sin instalación
    {"tipo": "pequeña", "potencia": 2.5, "prob": 0.25},        # 25% - 2.5 kWp (6-8 paneles)
    {"tipo": "mediana", "potencia": 4.5, "prob": 0.30},        # 30% - 4.5 kWp (12-15 paneles)
    {"tipo": "grande", "potencia": 6.5, "prob": 0.20},         # 20% - 6.5 kWp (16-20 paneles)
    {"tipo": "muy_grande", "potencia": 9.0, "prob": 0.05},     # 5% - 9.0 kWp (22-28 paneles)
]

# Barrios de Elche y alrededores
BARRIOS = [
    "Carrús", "Centro", "Altabix", "El Pla", "Raval", 
    "Sector Quinto", "Palmerales", "San Antón", "Los Palmerales",
    "El Toscar", "Puertas Coloradas", "Las Bayas", "Zona Norte"
]

CIUDADES = [
    {"ciudad": "Elche", "provincia": "Alicante", "cp": "03200"},
    {"ciudad": "Elche", "provincia": "Alicante", "cp": "03201"},
    {"ciudad": "Elche", "provincia": "Alicante", "cp": "03202"},
    {"ciudad": "Elche", "provincia": "Alicante", "cp": "03203"},
    {"ciudad": "Elche", "provincia": "Alicante", "cp": "03204"},
    {"ciudad": "Elche", "provincia": "Alicante", "cp": "03205"},
    {"ciudad": "Elche", "provincia": "Alicante", "cp": "03206"},
]

def seleccionar_tipo_ponderado(tipos):
    """Selecciona un tipo basado en probabilidades"""
    rand = random.random()
    acumulado = 0
    for tipo in tipos:
        acumulado += tipo["prob"]
        if rand <= acumulado:
            return tipo
    return tipos[-1]

def generar_clientes():
    """Genera el CSV de clientes con sus características"""
    clientes = []
    
    for i in range(NUM_CLIENTES):
        ciudad_info = random.choice(CIUDADES)
        
        # Asignar tipo de vivienda e instalación solar
        tipo_vivienda = seleccionar_tipo_ponderado(TIPOS_VIVIENDA)
        tipo_instalacion = seleccionar_tipo_ponderado(TIPOS_INSTALACION)
        
        # Generar nombre y dirección con Faker
        if i == 0:
            nombre = "Aitor Medrano"
            calle = "Secreta"
            barrio = "Carrús"
            cp = "03206"
        else:
            nombre = fake.name()
            calle = fake.street_name()
            barrio = random.choice(BARRIOS)
            cp = ciudad_info["cp"]
        
        cliente = {
            "_id": f"ObjectId('{i:024x}')",
            "nombre": nombre,
            "calle": calle,
            "numero": str(random.randint(1, 300)),
            "ciudad": ciudad_info["ciudad"],
            "barrio": barrio,
            "provincia": ciudad_info["provincia"],
            "cp": cp,
            "tipo_vivienda": tipo_vivienda,
            "tipo_instalacion": tipo_instalacion
        }
        clientes.append(cliente)
    
    # Escribir CSV de clientes (sin incluir tipos en el CSV, solo para cálculos internos)
    with open('clientes.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['_id', 'nombre', 'calle', 'numero', 'ciudad', 'barrio', 'provincia', 'cp'])
        writer.writeheader()
        for cliente in clientes:
            # Crear copia sin los campos de tipo
            cliente_csv = {k: v for k, v in cliente.items() if k not in ['tipo_vivienda', 'tipo_instalacion']}
            writer.writerow(cliente_csv)
    
    return clientes

def calcular_necesidad_red(consumo, generado):
    """Calcula la necesidad de red"""
    necesidad = consumo - generado
    return max(0, necesidad)

def generar_consumo_hora(hora, mes, tipo_vivienda):
    """Genera consumo realista según la hora del día, estación y tipo de vivienda"""
    
    # Factor estacional para calefacción/aire acondicionado
    factor_estacion = 1.0
    if mes in [12, 1, 2]:  # Invierno - calefacción
        factor_estacion = 1.4
    elif mes in [6, 7, 8]:  # Verano - aire acondicionado
        factor_estacion = 1.5
    elif mes in [3, 4, 5, 9, 10, 11]:  # Primavera/Otoño
        factor_estacion = 0.9
    
    # Factor por tipo de vivienda
    factor_tipo = tipo_vivienda["factor"]
    
    # Consumo base por hora (en kW)
    if 0 <= hora < 7:  # Madrugada (00:00-07:00)
        # Solo electrodomésticos básicos: nevera, standby
        base = random.uniform(0.3, 0.8)
        
    elif 7 <= hora < 9:  # Mañana temprana (07:00-09:00)
        # Desayuno, duchas, preparación para trabajo/colegio
        base = random.uniform(1.5, 3.5)
        # Picos: calentador agua, cafetera, tostadora, secador
        
    elif 9 <= hora < 14:  # Mañana-mediodía (09:00-14:00)
        # Casa más vacía, pero algunos electrodomésticos
        base = random.uniform(0.8, 1.8)
        # Lavadora, lavavajillas ocasional
        
    elif 14 <= hora < 17:  # Mediodía-tarde (14:00-17:00)
        # Comida, gente en casa
        base = random.uniform(1.2, 2.5)
        # Cocina (vitrocerámica/inducción), horno, microondas
        
    elif 17 <= hora < 21:  # Tarde (17:00-21:00)
        # Regreso del trabajo, actividad familiar
        base = random.uniform(1.5, 3.0)
        # TV, ordenadores, iluminación empieza
        
    elif 21 <= hora < 23:  # Noche temprana (21:00-23:00)
        # Cena, entretenimiento, pico nocturno
        base = random.uniform(2.0, 4.0)
        # Cocina, TV, todos los dispositivos, iluminación completa
        
    else:  # Noche (23:00-00:00)
        # Preparación para dormir
        base = random.uniform(1.0, 2.0)
        # Iluminación, TV, algunos dispositivos
    
    # Aplicar factores
    consumo = base * factor_estacion * factor_tipo
    
    # Añadir variabilidad aleatoria ±15%
    variacion = random.uniform(0.85, 1.15)
    consumo_final = consumo * variacion
    
    # Redondear a 2 decimales
    return round(consumo_final, 2)

def generar_generacion_hora(hora, mes, tipo_instalacion):
    """Genera energía solar realista según la hora, mes y tipo de instalación"""
    
    # Sin generación de noche
    if hora < 6 or hora >= 21:
        return 0.0
    
    # Horas de sol efectivas según estación
    if mes in [6, 7, 8]:  # Verano
        horas_sol_max = 14  # Más horas de luz
        radiacion_max = 1.0
    elif mes in [12, 1, 2]:  # Invierno
        horas_sol_max = 9
        radiacion_max = 0.5
    elif mes in [3, 4, 5]:  # Primavera
        horas_sol_max = 12
        radiacion_max = 0.85
    else:  # Otoño (9, 10, 11)
        horas_sol_max = 10
        radiacion_max = 0.7
    
    # Potencia instalada (kWp)
    potencia = tipo_instalacion["potencia"]
    
    # Curva de generación solar realista (eficiencia por hora)
    # Basada en la posición del sol
    if 6 <= hora < 8:  # Amanecer
        eficiencia = random.uniform(0.1, 0.25)
    elif 8 <= hora < 10:  # Mañana
        eficiencia = random.uniform(0.4, 0.65)
    elif 10 <= hora < 14:  # Mediodía - máxima generación
        eficiencia = random.uniform(0.75, 0.95)
    elif 14 <= hora < 17:  # Tarde
        eficiencia = random.uniform(0.5, 0.75)
    elif 17 <= hora < 19:  # Atardecer
        eficiencia = random.uniform(0.2, 0.45)
    else:  # 19-21 - últimas luces
        eficiencia = random.uniform(0.05, 0.15)
    
    # Factores de pérdida realistas
    factor_temperatura = random.uniform(0.85, 0.95)  # Pérdidas por temperatura
    factor_suciedad = random.uniform(0.92, 0.98)     # Polvo/suciedad en paneles
    factor_nubosidad = random.uniform(0.7, 1.0)      # Nubes ocasionales
    
    # Cálculo final
    generacion = (potencia * eficiencia * radiacion_max * 
                  factor_temperatura * factor_suciedad * factor_nubosidad)
    
    # Días ocasionales muy nublados/lluvia (5% de probabilidad)
    if random.random() < 0.05:
        generacion *= random.uniform(0.1, 0.3)
    
    return round(generacion, 2)

def generar_energia(clientes):
    """Genera el CSV de energía"""
    print("Generando datos de energía...")
    
    # Fecha inicial
    fecha_inicio = datetime(YEAR, 1, 1, 0, 0, 0)
    
    with open('energia.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['_id', 'propietario_id', 'date', 'consumo', 'generado', 'necesidad_red'])
        writer.writeheader()
        
        registro_id = 0
        
        # Para cada cliente
        for cliente_idx, cliente in enumerate(clientes):
            propietario_id = cliente["_id"]
            tipo_vivienda = cliente["tipo_vivienda"]
            tipo_instalacion = cliente["tipo_instalacion"]
            
            # Para cada día del año
            for dia in range(365):
                fecha_dia = fecha_inicio + timedelta(days=dia)
                
                # Para cada hora del día
                for hora in range(24):
                    fecha_completa = fecha_dia + timedelta(hours=hora)
                    
                    # Generar consumo y generación realistas
                    consumo = generar_consumo_hora(hora, fecha_completa.month, tipo_vivienda)
                    generado = generar_generacion_hora(hora, fecha_completa.month, tipo_instalacion)
                    necesidad_red = calcular_necesidad_red(consumo, generado)
                    
                    registro = {
                        "_id": f"ObjectId('{registro_id:024x}')",
                        "propietario_id": propietario_id,
                        "date": fecha_completa.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        "consumo": consumo,
                        "generado": generado,
                        "necesidad_red": necesidad_red
                    }
                    
                    writer.writerow(registro)
                    registro_id += 1
            
            if (cliente_idx + 1) % 50 == 0:
                print(f"Procesados {cliente_idx + 1} clientes... ({registro_id:,} registros)")
    
    print(f"\n✓ Archivo 'energia.csv' generado con {registro_id:,} registros")

def main():
    print("=" * 60)
    print("GENERADOR DE DATOS DE ENERGÍA SOLAR")
    print("=" * 60)
    print(f"\nConfiguracion:")
    print(f"- Clientes: {NUM_CLIENTES}")
    print(f"- Año: {YEAR}")
    print(f"- Registros esperados: {NUM_CLIENTES * 365 * 24:,}")
    print("\n" + "=" * 60 + "\n")
    
    # Generar clientes
    print("Generando clientes...")
    clientes = generar_clientes()
    print(f"✓ Archivo 'clientes.csv' generado con {len(clientes)} registros\n")
    
    # Generar energía
    generar_energia(clientes)
    
    print("\n" + "=" * 60)
    print("PROCESO COMPLETADO")
    print("=" * 60)
    print("\nArchivos generados:")
    print("1. clientes.csv")
    print("2. energia.csv")

if __name__ == "__main__":
    main()