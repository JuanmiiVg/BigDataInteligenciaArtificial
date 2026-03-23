import os
from pathlib import Path
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt


def default_parquet():
    repo_root = Path(__file__).resolve().parents[1]
    out_path = repo_root / "data" / "parquet" / "ventas"
    return str(out_path)


def main():
    parquet_path = default_parquet()
    print(f"Reading Parquet from: {parquet_path}")

    spark = SparkSession.builder.master("local[*]").appName("UD3-Lab3-Explore").getOrCreate()
    df = spark.read.parquet(parquet_path)

    print("Schema:")
    df.printSchema()

    print("Sample rows:")
    df.show(10)

    print("Filter importe > 100, group by ciudad:")
    from pyspark.sql.functions import col
    res = df.filter(col("importe") > 100).groupBy("ciudad").count().orderBy("count", ascending=False)
    res.show(20)

    # Plot total importe per ciudad (small result -> toPandas)
    agg = df.groupBy("ciudad").sum("importe").withColumnRenamed("sum(importe)", "total_importe").orderBy("total_importe", ascending=False)
    pdf = agg.toPandas()

    if not pdf.empty:
        os.makedirs(Path(parquet_path).parents[1] / "figures", exist_ok=True)
        fig_path = Path(parquet_path).parents[1] / "figures" / "ventas_por_ciudad.png"
        plt.figure(figsize=(10, 6))
        plt.bar(pdf["ciudad"].astype(str), pdf["total_importe"])
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Total importe")
        plt.title("Total importe por ciudad")
        plt.tight_layout()
        plt.savefig(fig_path)
        print(f"Saved plot to: {fig_path}")
    else:
        print("Aggregation returned no rows; skipping plot.")

    spark.stop()


if __name__ == "__main__":
    main()
