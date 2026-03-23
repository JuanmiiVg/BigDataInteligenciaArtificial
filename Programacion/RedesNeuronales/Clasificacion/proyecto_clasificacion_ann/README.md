# Proyecto Clasificación ANN

Este proyecto cumple la estructura de entrega de la actividad de clasificación con red neuronal MLP.

## Estructura

- `main.py`: script principal.
- `informe.md`: plantilla del informe técnico.
- `requirements.txt`: dependencias.
- `results/tensorboard/`: logs para TensorBoard.
- `results/graficas/`: gráficas de entrenamiento/evaluación.

## Dataset

Por defecto, si no pasas un CSV, se usa **Our World in Data (COVID-19)** con descarga automática.

Definición de objetivo binario por defecto:

- `target = 1` si `new_deaths_per_million >= 1.0`
- `target = 0` en caso contrario

También puedes usar:

- `--dataset-source sklearn` (dataset similar de prueba)
- `--data ... --target-col ...` (CSV propio)

## Variable objetivo usada

Para OWID, el objetivo binario se construye así:

- `target = 1` si `new_deaths_per_million >= 1.0`
- `target = 0` si `new_deaths_per_million < 1.0`

## Ejecución

1. Crear entorno virtual.
2. Instalar dependencias.
3. Ejecutar entrenamiento.
4. Abrir TensorBoard.

### Comandos (PowerShell)

```powershell
cd "c:\Users\usuario\Documents\BigData\Programación\RedesNeuronales\Clasificacion\proyecto_clasificacion_ann"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py --dataset-source owid --epochs 30 --batch-size 64 --owid-max-rows 120000 --output-dir ../ann_results
```

Con OWID y umbral personalizado:

```powershell
python main.py --dataset-source owid --owid-target-threshold 0.8 --owid-max-rows 100000
```

Con dataset propio:

```powershell
python main.py --data "ruta\a\tu_dataset.csv" --target-col "nombre_objetivo"
```

Con dataset similar de `sklearn`:

```powershell
python main.py --dataset-source sklearn
```

Abrir TensorBoard:

```powershell
tensorboard --logdir ../ann_results/tensorboard

```

## Qué genera

- `output_dir/metrics_summary.csv`: métricas de validación y test para:
  - MLP sin regularización
  - MLP con regularización (L2 + BatchNorm + Dropout)
  - Regresión logística (baseline)
- `output_dir/model_info.txt`: número de parámetros.
- `output_dir/graficas/*.png`: pérdida, accuracy, matrices de confusión y curvas ROC.

## Requisitos evaluados cubiertos

- Preprocesamiento con imputación, codificación categórica y estandarización.
- División `70/15/15` con estratificación.
- MLP con `ReLU` + salida `Sigmoid` + `Binary Crossentropy` + `Adam`.
- Comparación con y sin regularización.
- Métricas: Accuracy, Recall, Specificity, F1, AUC-ROC, matriz de confusión.
- Baseline clásico: Regresión logística.
- TensorBoard integrado.

## Resultados de la ejecución de prueba (OWID)

Ejecución realizada con:

- `--dataset-source owid --epochs 3 --batch-size 64 --owid-max-rows 20000 --output-dir ../ann_results`

Resumen (test):

- MLP base: Accuracy `0.9632`, Recall `0.4615`, Specificity `0.9947`, F1 `0.5970`, AUC `0.9082`.
- MLP regularizado: Accuracy `0.9591`, Recall `0.3692`, Specificity `0.9961`, F1 `0.5161`, AUC `0.9125`.
- Regresión logística: Accuracy `0.9482`, Recall `0.1538`, Specificity `0.9981`, F1 `0.2597`, AUC `0.8606`.

Archivos generados en:

- `../ann_results/metrics_summary.csv`
- `../ann_results/graficas/`
- `../ann_results/tensorboard/`
