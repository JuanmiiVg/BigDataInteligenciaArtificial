# clean_worldpop.py
import pandas as pd
import numpy as np
import re

INPUT_CSV = "population_data.csv"          # <- pon aquí tu archivo original
OUTPUT_CSV = "population_clean.csv"   # <- archivo resultante

def normalize_minus(s: str) -> str:
    # cambia signos menos Unicode (U+2212) a ascii '-' y limpia comillas
    if pd.isna(s):
        return s
    if not isinstance(s, str):
        return s
    s = s.replace('−', '-')   # minus unicode → ascii
    s = s.replace('—', '-')   # em-dash por si acaso
    s = s.replace('"', '')
    s = s.strip()
    return s

def unthousandize(s: str) -> str:
    # elimina separadores de miles si son parte de un número, p.ej. "1,234,567" -> "1234567"
    if pd.isna(s):
        return s
    if not isinstance(s, str):
        return s
    # si es algo con dígitos y comas (y opcional signo -), quitamos comas
    if re.match(r'^[\-\+]?[0-9]{1,3}(?:,[0-9]{3})+(?:\.[0-9]+)?$', s):
        return s.replace(',', '')
    return s

def parse_cell(s: str):
    # normaliza, detecta % y números, devuelve:
    #  - int (sin decimales) si el contenido es numérico o es porcentaje
    #  - NaN si vacío
    #  - el string original si no es numérico
    if pd.isna(s):
        return np.nan
    if not isinstance(s, str):
        # si ya es numérico
        try:
            return int(round(float(s)))
        except Exception:
            return s

    s = normalize_minus(s)
    s = s.strip()
    if s == "":
        return np.nan

    # quitar separadores miles en números con comas
    s = unthousandize(s)

    # si tiene porcentaje
    if s.endswith('%'):
        body = s[:-1].strip()
        # algunos porcentajes usan coma decimal en lugar de punto (ej 0,89%)
        body = body.replace(',', '.')
        try:
            f = float(body)
            # DECISIÓN: convertimos al entero redondeado del valor numérico
            # ej 0.89% -> 1  (si prefieres 0 en lugar de 1, cambia round->floor)
            return int(round(f))
        except:
            return s

    # si contiene coma decimal (ej "1,94") o punto decimal
    if re.match(r'^[\-\+]?[0-9]+[.,][0-9]+$', s):
        s2 = s.replace(',', '.')
        try:
            return int(round(float(s2)))
        except:
            return s

    # si es un entero con posible signo y/o separadores miles ya retirados
    if re.match(r'^[\-\+]?[0-9]+$', s):
        try:
            return int(s)
        except:
            return s

    # algunos valores pueden ser "−495,753" con la coma — ya manejado antes,
    # pero si algo más queda, devolvemos tal cual el string limpio.
    return s

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # aplicamos parse_cell a todas las celdas
    df_clean = df.applymap(lambda x: parse_cell(x))
    return df_clean

def main():
    # leemos todo como strings para poder limpiar
    df = pd.read_csv(INPUT_CSV, dtype=str, keep_default_na=False, na_values=["", " "])

    # Aplicar limpieza por columnas/por celdas
    df_clean = clean_dataframe(df)

    # Opcional: si quieres forzar tipos por columna (ej. Population 2025 -> int)
    # Aquí detectamos columnas enteras y las convertimos si es posible.
    for col in df_clean.columns:
        # si la columna contiene sólo ints/NaN, convertir a Int64 (nullable integer)
        non_na = df_clean[col].dropna()
        if non_na.apply(lambda v: isinstance(v, (int, np.integer))).all():
            df_clean[col] = df_clean[col].astype('Int64')  # tipo entero nullable
        # si mezcla strings y números, la dejamos como está.

    # Guardar resultado
    df_clean.to_csv(OUTPUT_CSV, index=False)
    print(f"Guardado CSV limpio en: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
