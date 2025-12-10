#!/usr/bin/env python3
"""
detectar_viviendas_bigdata_diario.py

Conexión: server25.fjortega.es:27777, BD "bigdata"
Colecciones: "clientes" y "consumos"

Requisitos:
    pip install pymongo pandas matplotlib

Uso:
    python detectar_viviendas_bigdata_diario.py
"""

from pymongo import MongoClient, ASCENDING, UpdateOne
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime
import re

# ---------- CONFIG ----------
MONGO_HOST = "server25.fjortega.es"
MONGO_PORT = 27777
DB_NAME = "bigdata"
COL_CLIENTES = "clientes"
COL_CONSUMOS = "consumos"
COL_DIARIOS = "consumos_diarios"

TOP_N_SUSPICIOS = 20
MIN_REGISTROS_POR_VIVIENDA = 240
NIGHT_HOURS = list(range(23,24)) + list(range(0,6))
NIGHT_RATIO_THRESHOLD = 1.5
PERCENTILE_AUTO = 99.0

OUT_DIR = "salida_sospechosos"
os.makedirs(OUT_DIR, exist_ok=True)

# ---------- Conexión ----------
def get_client():
    uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"
    return MongoClient(uri, serverSelectionTimeoutMS=5000)

# ---------- Detectar campos ----------
def detect_fields(coll):
    sample = coll.find_one()
    if not sample:
        raise RuntimeError("La colección de consumos está vacía o no se puede leer.")
    keys = set(sample.keys())
    owner_candidates = ["propietario_id", "propietario", "cliente_id", "cliente", "vivienda", "owner", "user_id"]
    date_candidates = ["date", "fecha", "timestamp", "ts", "datetime"]
    consumo_candidates = ["consumo", "consumption", "value", "kwh", "energia"]

    owner_field = next((k for k in owner_candidates if k in keys), None)
    date_field = next((k for k in date_candidates if k in keys), None)
    consumo_field = next((k for k in consumo_candidates if k in keys), None)

    if not owner_field:
        for k in keys:
            if k.startswith("_"):
                continue
            v = sample.get(k)
            if isinstance(v, str) and len(v) < 40:
                owner_field = k
                break
    if not date_field:
        for k in keys:
            v = sample.get(k)
            if isinstance(v, str) and ("T" in v and "-" in v and ":" in v):
                date_field = k
                break
            if hasattr(v, "isoformat"):
                date_field = k
                break
    if not consumo_field:
        for k in keys:
            v = sample.get(k)
            if isinstance(v, (int, float)) and not any(x in k.lower() for x in ("count","idx","index","num")):
                consumo_field = k
                break
    return owner_field, date_field, consumo_field

# ---------- Crear índices ----------
def ensure_indexes(coll, owner_field, date_field, consumo_field):
    try:
        if owner_field:
            coll.create_index([(owner_field, ASCENDING)], background=True)
        if date_field:
            coll.create_index([(date_field, ASCENDING)], background=True)
        if consumo_field:
            coll.create_index([(consumo_field, ASCENDING)], background=True)
        print("Índices creados sobre:", owner_field, date_field, consumo_field)
    except Exception as e:
        print("Error creando índices:", e)

# ---------- Conversion de fechas string ----------
def parse_iso_datetime(s):
    if not isinstance(s, str):
        return None
    s = s.strip().rstrip("Z")
    fmts = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"]
    for f in fmts:
        try:
            return datetime.strptime(s, f)
        except:
            continue
    return None

def convert_date_strings_to_bson(coll, date_field, batch_size=2000):
    cursor = coll.find({date_field: {"$type": "string"}}, {date_field: 1})
    ops = []
    total = 0
    for doc in cursor:
        raw = doc.get(date_field)
        dt = parse_iso_datetime(raw)
        if dt is None:
            continue
        ops.append(UpdateOne({"_id": doc["_id"]}, {"$set": {date_field: dt}}))
        total += 1
        if len(ops) >= batch_size:
            coll.bulk_write(ops, ordered=False)
            ops = []
            print(f"Actualizados {total} documentos...")
    if ops:
        coll.bulk_write(ops, ordered=False)
        print(f"Actualizados {total} documentos (último batch).")
    print("Conversión completa.")
    return total

# ---------- Agregación diaria ----------
def aggregate_to_daily(db, owner_field, date_field, consumo_field):
    coll = db[COL_CONSUMOS]
    # verificar si hay fechas como string
    sample = coll.find_one({date_field: {"$type": "string"}})
    if sample:
        print("Detectadas fechas string. Convertir a Date...")
        convert_date_strings_to_bson(coll, date_field)

    owner_ref = f"${owner_field}"
    consumo_ref = f"${consumo_field}"

    pipeline = [
        {"$addFields": {"day": {"$dateToString": {"format": "%Y-%m-%d", "date": f"${date_field}"}}}},
        {"$addFields": {"hour": {"$hour": f"${date_field}"}}},
        {"$group": {
            "_id": {"propietario_id": owner_ref, "day": "$day"},
            "sum_consumo": {"$sum": consumo_ref},
            "avg_consumo": {"$avg": consumo_ref},
            "max_consumo": {"$max": consumo_ref},
            "count_horas": {"$sum": 1},
            "sum_noche": {"$sum": {"$cond": [{"$in": ["$hour", NIGHT_HOURS]}, consumo_ref, 0]}}
        }},
        {"$project": {
            "_id": 0,
            "propietario_id": "$_id.propietario_id",
            "day": "$_id.day",
            "sum_consumo": 1,
            "avg_consumo": 1,
            "max_consumo": 1,
            "count_horas": 1,
            "sum_noche": 1,
            "pct_noche": {"$cond": [{"$gt": ["$sum_consumo", 0]}, {"$divide": ["$sum_noche", "$sum_consumo"]}, 0]}
        }},
        {"$merge": {"into": COL_DIARIOS, "on": ["propietario_id","day"], "whenMatched":"replace", "whenNotMatched":"insert"}}
    ]
    print("Ejecutando pipeline de agregación diaria...")
    coll.aggregate(pipeline, allowDiskUse=True)
    print("Agregación diaria completada.")

# ---------- Cargar métricas por propietario ----------
def load_stats_daily(db):
    coll = db[COL_DIARIOS]
    df = pd.DataFrame(list(coll.find()))
    if df.empty:
        return df
    df_group = df.groupby("propietario_id").agg(
        avg_consumo=("avg_consumo","mean"),
        max_consumo=("max_consumo","max"),
        count=("sum_consumo","count"),
        avg_noche=("pct_noche","mean")
    ).reset_index()
    df_group["night_ratio"] = df_group["avg_noche"] / df_group["avg_consumo"].replace({0:1e-9})
    return df_group

# ---------- Selección sospechosos ----------
def select_suspicious(stats_df):
    if stats_df.empty:
        return stats_df
    threshold = stats_df["avg_consumo"].quantile(PERCENTILE_AUTO/100.0)
    candidates = stats_df[stats_df["avg_consumo"] >= threshold].copy()
    extra = stats_df[stats_df["night_ratio"] >= NIGHT_RATIO_THRESHOLD].copy()
    combined = pd.concat([candidates, extra]).drop_duplicates(subset=["propietario_id"])
    med_avg = combined["avg_consumo"].median() if not combined["avg_consumo"].isnull().all() else 1
    med_night = combined["night_ratio"].median() if not combined["night_ratio"].isnull().all() else 1
    combined["suspicious_score"] = (combined["avg_consumo"]/med_avg)*0.6 + (combined["night_ratio"]/med_night)*0.4
    return combined.sort_values("suspicious_score",ascending=False).head(TOP_N_SUSPICIOS)

# ---------- Graficar ----------
def plot_series(df_series, propietario_id):
    if df_series.empty:
        return
    plt.figure(figsize=(12,4))
    plt.plot(df_series.index, df_series["avg_consumo"], linewidth=0.8)
    plt.title(f"Consumo horario medio - {propietario_id}")
    plt.xlabel("Fecha/hora")
    plt.ylabel("kW")
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR,f"{propietario_id}_consumo_horario.png")
    plt.savefig(out_path,dpi=150)
    plt.close()

def fetch_hourly_series(db, propietario_id):
    coll = db[COL_CONSUMOS]
    pipeline = [
        {"$match":{"propietario_id": propietario_id}},
        {"$sort":{"date":1}},
        {"$project":{"date":1,"consumo":1}}
    ]
    docs = list(coll.find({"propietario_id": propietario_id}))
    rows = []
    for d in docs:
        dt = d.get("date") if isinstance(d.get("date"), datetime) else parse_iso_datetime(d.get("date"))
        if dt:
            rows.append({"date": dt, "avg_consumo": d.get("consumo",0)})
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df.set_index("date", inplace=True)
    return df

# ---------- MAIN ----------
def main():
    client = get_client()
    try:
        client.server_info()
    except Exception as e:
        print("ERROR: no se puede conectar al servidor MongoDB:", e)
        sys.exit(1)

    db = client[DB_NAME]

    if COL_CONSUMOS not in db.list_collection_names():
        print(f"ERROR: La colección '{COL_CONSUMOS}' no existe.")
        sys.exit(1)

    coll = db[COL_CONSUMOS]

    owner_field, date_field, consumo_field = detect_fields(coll)
    print("Campos detectados:", owner_field, date_field, consumo_field)
    ensure_indexes(coll, owner_field, date_field, consumo_field)

    # Agregación diaria
    aggregate_to_daily(db, owner_field, date_field, consumo_field)

    # Cargar métricas por propietario
    stats_df = load_stats_daily(db)
    if stats_df.empty:
        print("No hay datos para generar estadísticas.")
        return

    # Seleccionar sospechosos
    suspicious = select_suspicious(stats_df)
    suspicious.to_csv(os.path.join(OUT_DIR,"viviendas_sospechosas.csv"),index=False)
    print("\nSospechosos identificados (resumen):")
    print(suspicious.to_string(index=False))

    # Graficar series horarias
    for _, row in suspicious.iterrows():
        prop = row["propietario_id"]
        df_series = fetch_hourly_series(db, prop)
        plot_series(df_series, prop)

    print("\nProceso finalizado. Revisar carpeta:", OUT_DIR)

if __name__ == "__main__":
    main()
