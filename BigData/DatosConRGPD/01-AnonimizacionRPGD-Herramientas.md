## 1️⃣ Script para generar el dataset grande y el ZIP

Guarda esto como `generar_dataset_rgpd.py` en un directorio vacío y ejecútalo con tu Python:

```python
#!/usr/bin/env python
import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import zipfile
from pathlib import Path

BASE = Path(".")
RGPD_ROOT = BASE / "rgpd_practica"
RGPD_ROOT.mkdir(parents=True, exist_ok=True)

random.seed(42)
np.random.seed(42)

# 1) Generar clientes_raw.csv (~300 clientes)
n_clients = 300

names = ["Ana","Juan","Carmen","Luis","Sara","Pedro","Marta","Raúl","Lucía","Diego",
         "Elena","Alberto","Patricia","Sergio","Noelia","Javier","Laura","Iván","Rosa","Manuel"]
surnames = ["López","Pérez","García","Rodríguez","Martín","Sánchez","Gómez","Ruiz","Hernández","Díaz",
            "Moreno","Álvarez","Romero","Navarro","Torres","Domínguez","Vázquez","Ramos","Gil","Castro"]
cities = ["Madrid","Sevilla","Valencia","Málaga","Bilbao","Zaragoza","Murcia","Valladolid"]
city_cp = {
    "Madrid": ["28001","28002","28003","28011","28012"],
    "Sevilla": ["41001","41002","41005","41010"],
    "Valencia": ["46001","46002","46021","46023"],
    "Málaga": ["29001","29002","29004","29010"],
    "Bilbao": ["48001","48002","48003"],
    "Zaragoza": ["50001","50002","50007"],
    "Murcia": ["30001","30002","30007"],
    "Valladolid": ["47001","47002","47010"],
}

rows_clientes = []
start_birth = datetime(1960,1,1)
end_birth = datetime(2005,12,31)
delta_birth = (end_birth - start_birth).days

for cid in range(1, n_clients+1):
    nombre = random.choice(names)
    apellido = random.choice(surnames)
    email = f"{nombre.lower()}.{apellido.lower()}_{cid}@example.com"
    telefono = "6" + "".join(str(random.randint(0,9)) for _ in range(8))
    birth_offset = random.randint(0, delta_birth)
    fecha_nacimiento = (start_birth + timedelta(days=birth_offset)).date().isoformat()
    ciudad = random.choice(cities)
    cod_postal = random.choice(city_cp[ciudad])
    gasto_mensual = round(random.uniform(20, 600), 2)
    frecuencia_compra = random.randint(0, 10)
    last_purchase_days = random.randint(0, 90)
    ultima_compra = (datetime(2025,3,1) - timedelta(days=last_purchase_days)).date().isoformat()

    rows_clientes.append({
        "id_cliente": cid,
        "nombre": nombre,
        "apellidos": apellido,
        "email": email,
        "telefono": telefono,
        "fecha_nacimiento": fecha_nacimiento,
        "ciudad": ciudad,
        "cod_postal": cod_postal,
        "gasto_mensual": gasto_mensual,
        "frecuencia_compra": frecuencia_compra,
        "ultima_compra": ultima_compra
    })

clientes_df = pd.DataFrame(rows_clientes)
clientes_path = RGPD_ROOT / "clientes_raw.csv"
clientes_df.to_csv(clientes_path, index=False)

print(f"[OK] Generado {clientes_path} con {len(clientes_df)} filas")

# 2) Generar ventas_clientes.csv (~1000 filas)
n_sales = 1000
channels = ["tienda","web","app"]

rows_ventas = []
start_sales_date = datetime(2025,1,1)

for i in range(1, n_sales+1):
    cid = random.randint(1, n_clients)
    fecha = start_sales_date + timedelta(days=random.randint(0, 59))  # Ene–Feb 2025
    importe = round(random.uniform(5, 300), 2)
    unidades = random.randint(1, 10)
    canal = random.choice(channels)

    ciudad = clientes_df.loc[cid-1, "ciudad"]
    cp = clientes_df.loc[cid-1, "cod_postal"]
    municipio_id = int(str(cp)[:3])

    rows_ventas.append({
        "id_venta": i,
        "id_cliente": cid,
        "fecha": fecha.date().isoformat(),
        "unidades": unidades,
        "importe": importe,
        "canal": canal,
        "ciudad": ciudad,
        "cod_postal": cp,
        "municipio_id": municipio_id
    })

ventas_df = pd.DataFrame(rows_ventas)
ventas_path = RGPD_ROOT / "ventas_clientes.csv"
ventas_df.to_csv(ventas_path, index=False)

print(f"[OK] Generado {ventas_path} con {len(ventas_df)} filas")

# 3) README
readme_text = """# Actividad RGPD: Anonimización y uso del dataset en calidad e integración

Contenido:

- `clientes_raw.csv`: dataset con datos personales (~300 clientes).
- `ventas_clientes.csv`: ~1000 ventas asociadas a esos clientes.

Sugerencia de uso:

1. Anonimizar `clientes_raw.csv`:
   - crear `id_hash` con hash de `id_cliente`,
   - eliminar nombre, apellidos, email, teléfono,
   - generalizar código postal (3 dígitos) y/o fecha de nacimiento (décadas).

2. Integrar con `ventas_clientes.csv`:
   - reemplazar `id_cliente` por `id_hash` en la tabla de ventas,
   - obtener `ventas_clientes_anon.csv`.

3. Reutilizar `ventas_clientes_anon.csv` en prácticas de:
   - calidad de datos (reglas de dominio, rango, consistencia),
   - integración con otras fuentes.
"""

with open(RGPD_ROOT / "README_RGPD_anonimizacion.md", "w", encoding="utf-8") as f:
    f.write(readme_text)

# 4) Empaquetar en ZIP
zip_path = BASE / "rgpd_practica_anonimizacion_full.zip"
with zipfile.ZipFile(zip_path, "w") as z:
    for root, dirs, files in os.walk(RGPD_ROOT):
        for file in files:
            full = Path(root) / file
            z.write(full, full.relative_to(BASE))

print(f"[OK] ZIP generado en: {zip_path}")
```

Ejecución:

```bash
python generar_dataset_rgpd.py
```

Te generará:

* carpeta `rgpd_practica/`

  * `clientes_raw.csv` (~300 filas)
  * `ventas_clientes.csv` (~1000 filas)
  * `README_RGPD_anonimizacion.md`
* fichero `rgpd_practica_anonimizacion_full.zip` listo para subir a Moodle/GitHub.

---

## 2️⃣ Notebook plantilla para la actividad (anonimización + integración + calidad)

Crea un archivo `anonimizacion_integracion.ipynb` y pega este contenido en un `.ipynb` vía Jupyter, o simplemente crea el notebook a mano copiando cada celda.

### Celda 1 – Markdown

```markdown
# Actividad RGPD: Anonimización e integración de datos

Trabajaremos con:

- `rgpd_practica/clientes_raw.csv`
- `rgpd_practica/ventas_clientes.csv`

Objetivos:

1. Identificar datos personales y columnas sensibles.
2. Aplicar anonimización (hash, eliminación, generalización).
3. Generar `clientes_anon.csv`.
4. Integrar las ventas con el identificador anónimo.
5. Aplicar reglas de calidad sobre el dataset integrado.
```

### Celda 2 – Carga de datos

```python
import pandas as pd
from pathlib import Path
import hashlib

base_path = Path("rgpd_practica")

clientes = pd.read_csv(base_path / "clientes_raw.csv")
ventas = pd.read_csv(base_path / "ventas_clientes.csv")

clientes.head(), ventas.head()
```

### Celda 3 – Identificación de datos personales (texto)

```markdown
## 1. Identificación de datos personales

En tu informe (fuera del notebook) clasifica las columnas de `clientes_raw.csv` en:

- Datos personales directos
- Datos personales indirectos
- Datos no personales

Explica brevemente por qué.
```

### Celda 4 – Crear id_hash

```python
def make_hash(x: int) -> str:
    return hashlib.sha256(str(x).encode()).hexdigest()

clientes["id_hash"] = clientes["id_cliente"].apply(make_hash)
clientes[["id_cliente", "id_hash"]].head()
```

### Celda 5 – Eliminación / generalización

```python
# Generalizar código postal a los 3 primeros dígitos
clientes["cp_trunc"] = clientes["cod_postal"].astype(str).str[:3]

# (Opcional) generalizar fecha de nacimiento a década
clientes["decada_nacimiento"] = clientes["fecha_nacimiento"].str[:3] + "0s"

# Dataset anonimizado: elimina columnas directas
cols_drop = ["nombre", "apellidos", "email", "telefono", "cod_postal", "fecha_nacimiento"]
clientes_anon = clientes.drop(columns=cols_drop)

clientes_anon.head()
```

### Celda 6 – Integración con ventas usando id_hash

```python
ventas_hash = ventas.merge(
    clientes_anon[["id_cliente", "id_hash", "ciudad", "cp_trunc", "decada_nacimiento"]],
    on="id_cliente",
    how="left"
)

# Eliminar id_cliente en la tabla final (ya tenemos id_hash)
ventas_hash = ventas_hash.drop(columns=["id_cliente"])

ventas_hash.head()
```

### Celda 7 – Reglas de calidad

```python
total = len(ventas_hash)
dom_canal = (ventas_hash["canal"].isin(["tienda", "web", "app"])).mean()
rango_unidades = (ventas_hash["unidades"] >= 0).mean()
importe_pos = (ventas_hash["importe"] > 0).mean()

print(f"Total registros: {total}")
print(f"Dominio canal correcto: {dom_canal:.2%}")
print(f"Unidades >= 0: {rango_unidades:.2%}")
print(f"Importe > 0: {importe_pos:.2%}")
```

### Celda 8 – Guardar datasets

```python
clientes_anon_path = base_path / "clientes_anon.csv"
ventas_hash_path = base_path / "ventas_clientes_anon.csv"

clientes_anon.to_csv(clientes_anon_path, index=False)
ventas_hash.to_csv(ventas_hash_path, index=False)

clientes_anon_path, ventas_hash_path
```

Con esto ya tienes:

* `clientes_anon.csv` (sin datos personales directos).
* `ventas_clientes_anon.csv` (para usar en la práctica de **calidad e integración**).

---

## 3️⃣ Cómo reutilizar el dataset en tu práctica de calidad / integración

Una vez generados `ventas_clientes_anon.csv`, puedes:

* Moverlo/copiarlo a `data_lake/raw/ventas/` como una fuente más.
* Aplicar las mismas reglas de calidad que en la práctica de ventas/turismo:

  * dominio en `canal`,
  * rangos de `unidades` e `importe`,
  * integridad frente a otras fuentes, etc.

