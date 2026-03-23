# Pack de clase: Mage AI con Docker Compose

## Qué incluye
- `docker-compose.yml`: despliegue local de Mage AI.
- `data/supermarket_sales_small.csv`: dataset pequeño para la práctica.
- `notebooks/01_mage_ai_profesor.ipynb`: notebook completo, guiado y resuelto.
- `notebooks/01_mage_ai_alumno.ipynb`: notebook de trabajo para el alumnado.
- `requirements.txt`: dependencias opcionales para ampliaciones del proyecto.

## Requisitos
- Docker
- Docker Compose

## Arranque
```bash
docker compose up
```

Después abre:
- http://localhost:6789

## Qué hace el contenedor
1. Si el proyecto `mage_project` no existe todavía, lo crea con `mage start mage_project`.
2. Arranca Mage en el puerto `6789`.
3. Monta:
   - `./mage_project` dentro del contenedor
   - `./data` para acceder al CSV de ejemplo

## Sugerencia de práctica en Mage
Crea un pipeline batch llamado `ventas_supermercado` con tres bloques:

### 1) Data Loader
```python
import pandas as pd

def load_data(*args, **kwargs):
    return pd.read_csv('/home/src/data/supermarket_sales_small.csv')
```

### 2) Transformer
```python
def transform(df, *args, **kwargs):
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['ingreso_neto_estimado'] = df['Total'] - df['Tax 5%']
    resumen = (
        df.groupby('Product line', as_index=False)
        .agg(
            ventas_totales=('Total', 'sum'),
            media_rating=('Rating', 'mean'),
            tickets=('Invoice ID', 'count')
        )
        .sort_values('ventas_totales', ascending=False)
    )
    return resumen
```

### 3) Data Exporter
```python
def export_data(df, *args, **kwargs):
    output_path = '/home/src/data/resumen_product_line.csv'
    df.to_csv(output_path, index=False)
    print(f'Fichero exportado en: {output_path}')
    print(df)
```

## Parada
```bash
docker compose down
```
