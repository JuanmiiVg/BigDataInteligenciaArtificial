import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    df = data.copy()

    # Fecha
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])

    # Convertir columnas numéricas (por si vienen como texto)
    cols_numericas = ['Total', 'Tax 5%', 'Rating']
    for c in cols_numericas:
        df[c] = pd.to_numeric(df[c], errors='coerce')

    # Eliminar filas con nulos en columnas clave tras conversión
    df = df.dropna(subset=['Total', 'Tax 5%', 'Rating'])

    # Métrica derivada
    df['ingreso_neto_estimado'] = df['Total'] - df['Tax 5%']

    # Resumen
    resumen = (
        df.groupby(['City', 'Product line'], as_index=False)
        .agg(
            ventas_totales=('Total', 'sum'),
            ingreso_neto_total=('ingreso_neto_estimado', 'sum'),
            rating_medio=('Rating', 'mean'),
            tickets=('Invoice ID', 'count'),
        )
        .sort_values(['ventas_totales', 'tickets'], ascending=[False, False])
    )

    return resumen


@test
def test_output(output, *args) -> None:
    assert output is not None, 'El output es None'
    assert len(output) > 0, 'El output está vacío'
    assert 'ventas_totales' in output.columns, 'Falta ventas_totales'