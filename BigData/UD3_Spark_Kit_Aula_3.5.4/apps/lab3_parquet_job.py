import argparse
import os
from pathlib import Path
from pyspark.sql import SparkSession


def default_paths():
    repo_root = Path(__file__).resolve().parents[1]
    data_path = repo_root / "data" / "ventas_clientes_anon_big.csv"
    out_path = repo_root / "data" / "parquet" / "ventas"
    return str(data_path), str(out_path)


def main():
    parser = argparse.ArgumentParser(description="Lab3: CSV -> Parquet (local)")
    default_input, default_output = default_paths()
    parser.add_argument("--input", "-i", default=default_input, help="Path to input CSV")
    parser.add_argument("--output", "-o", default=default_output, help="Path to output Parquet dir")
    parser.add_argument("--partition", "-p", action="store_true", help="Partition output by 'ciudad'")
    args = parser.parse_args()

    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Partition by ciudad: {args.partition}")

    spark = SparkSession.builder.master("local[*]").appName("UD3-Lab3-Parquet").getOrCreate()

    df = spark.read.csv(args.input, header=True, inferSchema=True)
    print("Schema:")
    df.printSchema()

    out_dir = args.output
    # Ensure parent directory exists
    os.makedirs(out_dir, exist_ok=True)

    write_builder = df.write.mode("overwrite")
    if args.partition:
        write_builder = write_builder.partitionBy("ciudad")

    write_builder.parquet(out_dir)

    print("Parquet write complete.")
    spark.stop()


if __name__ == "__main__":
    main()
