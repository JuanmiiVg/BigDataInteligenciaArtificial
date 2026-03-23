from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, avg as _avg, count as _count

DATA_PATH = "/opt/spark-data/ventas_clientes_anon.csv"

spark = SparkSession.builder.appName("UD3-Lab1").getOrCreate()
df = spark.read.csv(DATA_PATH, header=True, inferSchema=True)

df_f = df.filter(col("importe") > 100)

res = df_f.groupBy("ciudad").agg(
    _count("*").alias("num_ventas"),
    _sum("importe").alias("importe_total"),
    _avg("importe").alias("importe_medio")
).orderBy(col("importe_total").desc())

res.show(20)
res.coalesce(1).write.mode("overwrite").option("header", True).csv("/opt/spark-data/output/ventas_por_ciudad")

spark.stop()
