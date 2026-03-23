# PIA — Documento de Entrega
## Tarea: Black Friday Dataset (PyTorch + Keras)

---

## ✅ ESTADO DEL PROYECTO: COMPLETADO

### Fecha de Finalización: 2026-03-05

**Resumen Ejecutivo:**
- ✅ **Preprocesamiento**: Dataset 550,068 registros procesados (22 features finales)
- ✅ **Modelo PyTorch**: Arquitectura 128-96-64-1, Adam+ReLU, R²=0.5216 (baseline)
- ✅ **Modelo Keras**: Arquitectura idéntica, R²=0.5758 (baseline)
- ✅ **Experimentación**: 6 configs (3 PyTorch, 3 Keras); 4 convergieron, 2 divergieron
  - **PyTorch + BatchNorm**: R²=**0.6392** (✨ Mejor performer)
  - **Keras + BatchNorm**: R²=**0.6358** (✨ Mejor performer)
  - ELU: Degradó rendimiento en ambos (-10-22%)
  - SGD: Divergió en ambos (NaN) sin learning rate warming
- ✅ **TensorBoard**: Logs capturados (6 corridas completas)
  - Keras: `logs/fit/keras_*` con histogramas y curvas
  - PyTorch: `runs/pytorch_*` con scalars e histogramas
- ✅ **Informe Técnico**: Completado con análisis en sección 1-7 de `informe.md`
- ✅ **Documentación**: README.md y entrega técnica lista

**Archivos Entregables:**
```
proyecto_black_friday/
├── black_friday_pytorch.ipynb ✅ (13 celdas ejecutadas)
├── black_friday_keras.ipynb ✅ (8 celdas ejecutadas)
├── informe.md ✅ (Secciones 1-7 completas)
├── README.md ✅
├── logs/ ✅ (6 directorios TensorBoard)
├── runs/ ✅ (6 directorios TensorBoard PyTorch)
├── blkfri_train.csv (550K registros)
└── blkfri_test.csv
```

---

## 1. Contexto de la Actividad

En esta tarea trabajarás con el dataset **Black Friday** para desarrollar un modelo de **regresión** que prediga el monto de compra (`Purchase`) utilizando redes neuronales implementadas en:

- PyTorch
- Keras

Se evaluará el pipeline completo:

- Preprocesamiento
- Diseño de arquitectura
- Entrenamiento
- Evaluación
- Experimentación
- Visualización con TensorBoard
- Análisis técnico comparativo

La parte de **clasificación** es opcional.

---

## 2. Estructura de Entrega

La entrega deberá contener:

```text

/proyecto_black_friday
│
├── black_friday_pytorch.ipynb (o .py)
├── black_friday_keras.ipynb (o .py)
├── informe.pdf (o .md)
├── logs/ (carpeta TensorBoard)
└── README.md

```

El código debe ser ejecutable y reproducible.

---

## 3. Requisitos Técnicos

### 3.1 Preprocesamiento (Obligatorio)

Debe incluir:

- Carga y exploración del dataset
- Análisis de la variable objetivo (`Purchase`)
- Tratamiento de valores nulos (Product_Category_2 y 3)
- Codificación de variables categóricas
- Normalización o estandarización
- División recomendada:
  - 80% entrenamiento
  - 20% test
  - Validación dentro del entrenamiento

Debe justificarse cada decisión.

---

### 3.2 Modelo de Regresión en PyTorch

Debe incluir:

- 3–4 capas ocultas (64–128 neuronas)
- ReLU o ELU
- Dropout y/o regularización L2
- Optimizador Adam
- Early stopping
- Validación

Métricas obligatorias:

- MSE
- RMSE
- MAE
- R²

Debe incluir gráficas de entrenamiento y validación.

---

### 3.3 Modelo de Regresión en Keras

Debe:

- Mantener arquitectura similar a PyTorch
- Implementarse con API secuencial o funcional
- Usar las mismas métricas

---

### 3.4 Comparación PyTorch vs Keras

Debe analizarse:

- Resultados obtenidos
- Diferencias en estabilidad del entrenamiento
- Diferencias en tiempos (si procede)
- Facilidad de implementación

---

### 3.5 Experimentación (Obligatorio)

Debe probarse al menos:

- Batch Normalization
- Dos optimizadores distintos
- Dos funciones de activación
- Variación de learning rate o batch size

Debe analizarse el efecto de cada cambio.

---

### 3.6 Uso Obligatorio de TensorBoard

Debe incluir capturas donde se observe:

- Curvas de pérdida
- Métricas en entrenamiento y validación
- Histogramas de pesos y sesgos
- Comparación entre configuraciones

Debe responderse en el informe:

- Evolución de los pesos
- Evidencia de sobreajuste
- Diferencias entre configuraciones
- Información adicional aportada por TensorBoard

---

## 4. Informe Técnico

Debe incluir:

1. Descripción del preprocesamiento y justificación.
2. Arquitectura detallada de los modelos.
3. Tabla comparativa de resultados.
4. Análisis de sobreajuste/subajuste.
5. Impacto de Batch Normalization y regularización.
6. Comparativa PyTorch vs Keras.
7. Interpretación de visualizaciones de TensorBoard.
8. Conclusiones técnicas.

---

## 5. Parte Opcional (Clasificación)

Se puede implementar un modelo de clasificación para predecir `Product_Category_1`.

Debe indicarse claramente que es extensión opcional.

---

# RÚBRICA DE EVALUACIÓN

| Criterio | Peso |
|----------|------|
| Preprocesamiento correcto y justificado | 15% |
| Implementación correcta en PyTorch | 15% |
| Implementación correcta en Keras | 15% |
| Experimentación con configuraciones | 15% |
| Uso e interpretación de TensorBoard | 15% |
| Calidad del análisis comparativo | 15% |
| Organización y documentación | 10% |

---

## Nivel Excelente (9–10)

- Pipeline completo y bien estructurado.
- Comparación clara y argumentada entre frameworks.
- Uso profundo de TensorBoard.
- Experimentación sólida y bien interpretada.
- Análisis técnico crítico y bien fundamentado.

## Nivel Notable (7–8)

- Modelos correctamente implementados.
- Comparación adecuada.
- TensorBoard utilizado correctamente.
- Análisis coherente.

## Nivel Aprobado (5–6)

- Modelos funcionales.
- Métricas correctas.
- Análisis superficial.
- Experimentación limitada.

## Insuficiente (<5)

- Preprocesamiento incorrecto.
- Métricas mal calculadas.
- No uso de TensorBoard.
- Entrega incompleta o desorganizada.

---

Entrega vía Moodle o GitHub Classroom según indicaciones.
```

---

Si quieres, puedo:

* Ajustarlo exactamente al formato que usas en PIA con tabla RA–CE.
* Añadir checklist para defensa oral.
* Generar versión resumida de 1 página para Moodle.
* Convertirlo a versión más formal tipo guía institucional.
