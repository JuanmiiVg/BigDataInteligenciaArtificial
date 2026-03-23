import pandas as pd
import time

start = time.time()

df = pd.read_csv("data/ventas_clientes_anon_big.csv")

df_f = df[df["importe"] > 100]

res = (
    df_f.groupby("ciudad")
    .agg(
        num_ventas=("importe", "count"),
        importe_total=("importe", "sum"),
        importe_medio=("importe", "mean")
    )
    .sort_values("importe_total", ascending=False)
)

print(res.head(10))

end = time.time()
print(f"Tiempo total pandas: {end - start:.2f} segundos")
