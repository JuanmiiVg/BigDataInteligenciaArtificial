# Proyecto Black Friday — Guía Rápida

## Estructura esperada

```text
proyecto_black_friday/
├── black_friday_pytorch.ipynb   # o .py
├── black_friday_keras.ipynb     # o .py
├── informe.md
├── logs/fit/                    # TensorBoard Keras
├── runs/                        # TensorBoard PyTorch
└── README.md
```

## Flujo recomendado (paso a paso)

1. Cargar `SAA/blkfri_train.csv` y explorar nulos/distribuciones.
2. Definir preprocesamiento reproducible:
   - imputación de `Product_Category_2` y `Product_Category_3`
   - codificación categórica
   - escalado numérico
3. Dividir datos: `train/test = 80/20` y `val` dentro de `train`.
4. Entrenar modelo base en PyTorch (Adam + early stopping).
5. Entrenar modelo base equivalente en Keras.
6. Ejecutar experimentos (BatchNorm, activación, optimizador, LR o batch size).
7. Registrar todo en TensorBoard (métricas + histogramas).
8. Completar tabla comparativa y conclusiones en `informe.md`.

## Métricas obligatorias
- MSE
- RMSE
- MAE
- R²

## Comandos TensorBoard

```bash
# Keras
tensorboard --logdir=logs/fit

# PyTorch
tensorboard --logdir=runs
```

## Criterio para una entrega fuerte
- Misma base de datos y particiones para ambos frameworks.
- Arquitectura equivalente en PyTorch/Keras para comparación justa.
- Experimentos controlados (cambias 1 variable por experimento).
- Conclusiones respaldadas por métricas + gráficas + TensorBoard.
