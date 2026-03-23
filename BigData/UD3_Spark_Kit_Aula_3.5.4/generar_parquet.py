import pandas as pd
import os

# Leer CSV
df = pd.read_csv('data/ventas_clientes_anon_big.csv')

# Crear directorio Parquet si no existe
os.makedirs('data/parquet/ventas', exist_ok=True)

# Guardar como Parquet
df.to_parquet('data/parquet/ventas/data.parquet', index=False)

# Mostrar info
print('=== PARQUET GENERADO ===')
print(f'Registros: {len(df)}')
print(f'Columnas: {list(df.columns)}')
print(f'Tamaño (bytes): {os.path.getsize("data/parquet/ventas/data.parquet")}')
print()
print('=== PRIMERAS 5 FILAS ===')
print(df.head(5).to_string())
print()
print('=== ESQUEMA ===')
print(df.dtypes)
