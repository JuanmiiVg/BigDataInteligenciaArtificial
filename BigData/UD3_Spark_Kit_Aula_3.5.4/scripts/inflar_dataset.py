#!/usr/bin/env python3
import argparse
from datetime import timedelta
import pandas as pd
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--factor", type=int, default=100)
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    frames = []
    n = len(df)
    rng = np.random.default_rng(42)

    for i in range(args.factor):
        chunk = df.copy()
        if "fecha" in chunk.columns:
            chunk["fecha"] = pd.to_datetime(chunk["fecha"]) + pd.to_timedelta(rng.integers(0, 30, size=n), unit="D")
            chunk["fecha"] = chunk["fecha"].dt.strftime("%Y-%m-%d")
        if "importe" in chunk.columns:
            chunk["importe"] = (chunk["importe"] * rng.normal(1.0, 0.05, size=n)).round(2)
        frames.append(chunk)

    out = pd.concat(frames, ignore_index=True)
    out.to_csv(args.output, index=False)
    print(f"Generado {args.output} con {len(out)} filas")

if __name__ == "__main__":
    main()
