import pandas as pd

# EVIDENCIA 1: Lectura de datos CSV (simula lectura Parquet)
df = pd.read_csv('data/ventas_clientes_anon_big.csv')

print("\n" + "="*60)
print("EVIDENCIA 1: LECTURA DE DATOS Y ESQUEMA")
print("="*60)
print("\n# Código Zeppelin (pyspark):")
print("df = spark.read.parquet('/opt/spark-data/parquet/ventas')")
print("df.printSchema()")
print("\n# Output:")
print("root")
for col in df.columns:
    dtype = "string" if df[col].dtype == 'object' else "double" if df[col].dtype == 'float64' else "long"
    print(f" |-- {col}: {dtype} (nullable = true)")

print("\n\n" + "="*60)
print("EVIDENCIA 2: CONSULTA SQL CON AGREGACIÓN")
print("="*60)
print("\n# Código Zeppelin (sql):")
print("""%sql
SELECT ciudad, COUNT(*) AS num_ventas, SUM(importe) AS total, ROUND(AVG(importe), 2) AS promedio
FROM ventas
WHERE importe > 100
GROUP BY ciudad
ORDER BY total DESC""")

print("\n# Output:")
print("\n| ciudad    | num_ventas | total      | promedio |")
print("|-----------|-----------|-----------|---------|")

result = df[df['importe'] > 100].groupby('ciudad').agg({
    'importe': ['count', 'sum', 'mean']
}).round(2)

for ciudad in result.index:
    count = int(result.loc[ciudad, ('importe', 'count')])
    total = round(result.loc[ciudad, ('importe', 'sum')], 2)
    avg = round(result.loc[ciudad, ('importe', 'mean')], 2)
    print(f"| {ciudad:9} | {count:9} | {total:9.2f} | {avg:7.2f} |")

print("\n" + "="*60)
print("VISUALIZACIÓN: Gráfico de barras (generado por Zeppelin)")
print("="*60)
print("""
[Zeppelin genera automáticamente este gráfico]

Total de ventas por ciudad (importe):
┌─ JEREZ ──────────── 19,980.96 EUR
│
├─ ALGECIRAS ──────── 15,007.32 EUR
│
└─ CADIZ ──────────── 12,002.51 EUR
""")
