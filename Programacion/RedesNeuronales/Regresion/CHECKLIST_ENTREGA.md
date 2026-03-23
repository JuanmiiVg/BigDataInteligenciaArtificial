# Checklist de Entrega — Black Friday (PyTorch + Keras)

Marca cada punto antes de entregar.

## 1) Estructura del proyecto
- [ ] Existe carpeta `proyecto_black_friday/`
- [ ] Archivo `black_friday_pytorch.ipynb` o `.py`
- [ ] Archivo `black_friday_keras.ipynb` o `.py`
- [ ] Archivo `informe.md` (o PDF final)
- [ ] Carpeta de logs TensorBoard (`logs/` y/o `runs/`)
- [ ] `README.md` con instrucciones de ejecución

## 2) Preprocesamiento (obligatorio)
- [ ] Carga del dataset `SAA/blkfri_train.csv`
- [ ] EDA básico (distribuciones, tipos, nulos)
- [ ] Tratamiento de nulos en `Product_Category_2` y `Product_Category_3`
- [ ] Codificación de variables categóricas (`Gender`, `Age`, `City_Category`, `Stay_In_Current_City_Years`)
- [ ] Normalización/estandarización de variables numéricas
- [ ] División de datos: train/test (80/20) y validación dentro de train
- [ ] Justificación escrita de decisiones de preprocesamiento

## 3) Modelo PyTorch (obligatorio)
- [ ] Red de 3–4 capas ocultas (64–128 neuronas)
- [ ] Activación ReLU o ELU
- [ ] Regularización (Dropout y/o L2)
- [ ] Optimizador Adam
- [ ] Early stopping
- [ ] Métricas: MSE, RMSE, MAE, R²
- [ ] Curvas de entrenamiento y validación

## 4) Modelo Keras (obligatorio)
- [ ] Arquitectura equivalente a PyTorch
- [ ] API secuencial o funcional
- [ ] Métricas: MSE, RMSE, MAE, R²
- [ ] Curvas de entrenamiento y validación

## 5) Experimentación (obligatorio)
- [ ] Batch Normalization (con vs sin)
- [ ] Al menos 2 optimizadores (ej. Adam vs SGD)
- [ ] Al menos 2 activaciones (ej. ReLU vs ELU)
- [ ] Ajuste de learning rate o batch size
- [ ] Tabla comparativa de resultados por configuración

## 6) TensorBoard (obligatorio)
- [ ] Keras: callback `TensorBoard(histogram_freq=1)`
- [ ] PyTorch: `SummaryWriter`
- [ ] Logs de entrenamiento y validación
- [ ] Histogramas de pesos/sesgos
- [ ] Capturas incluidas en informe
- [ ] Respuestas a preguntas de interpretación (sobreajuste, saturación, etc.)

## 7) Informe técnico (obligatorio)
- [ ] Preprocesamiento y justificaciones
- [ ] Arquitecturas detalladas
- [ ] Tabla comparativa PyTorch vs Keras
- [ ] Análisis sobreajuste/subajuste
- [ ] Impacto de BatchNorm y regularización
- [ ] Interpretación de TensorBoard
- [ ] Conclusiones técnicas

## 8) Control final antes de subir
- [ ] Ejecuta notebooks/scripts desde cero sin errores
- [ ] Verifica que rutas y logs existen
- [ ] Verifica que las métricas del informe coinciden con el código
- [ ] Revisa ortografía y claridad del análisis
