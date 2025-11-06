import duckdb
import time

con = duckdb.connect()

file_csv = 'data/orders_flat.csv'
file_parquet = 'data/orders_flat.parquet'

query = """
SELECT customer_id, SUM(qty * price) AS total_spent
FROM read_csv_auto('{file}')
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 5
"""

def run_query(file):
    q = query.format(file=file)
    start = time.time()
    con.execute(q)
    result = con.fetchall()
    end = time.time()
    print(f"Tiempo ejecución con {file}: {end - start:.3f} segundos")
    print(result)

print("Primera ejecución con CSV")
run_query(file_csv)

print("\nSegunda ejecución con CSV")
run_query(file_csv)

print("\nPrimera ejecución con Parquet")
# Usar read_parquet para parquet
query_parquet = """
SELECT customer_id, SUM(qty * price) AS total_spent
FROM read_parquet('{file}')
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 5
"""

def run_query_parquet(file):
    q = query_parquet.format(file=file)
    start = time.time()
    con.execute(q)
    result = con.fetchall()
    end = time.time()
    print(f"Tiempo ejecución con {file}: {end - start:.3f} segundos")
    print(result)

run_query_parquet(file_parquet)

print("\nSegunda ejecución con Parquet")
run_query_parquet(file_parquet)
