if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):
    output_path = '/home/src/data/resumen_ventas_por_ciudad_y_linea.csv'
    data.to_csv(output_path, index=False)
    print('Exportado en:', output_path)
    print(data.head(10))
    return data