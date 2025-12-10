### 📘 Actividad Práctica – Preparación de Datos y Modelado para Clasificación

**Objetivo:**
Aplicar todo el flujo de trabajo de ciencia de datos desde el análisis exploratorio hasta el entrenamiento optimizado de un modelo de clasificación, siguiendo el ejemplo trabajado con el dataset *Titanic*.

---

### 📂 Dataset sugerido: **Bank Marketing (UCI)**

📥 [https://archive.ics.uci.edu/ml/datasets/bank+marketing](https://archive.ics.uci.edu/ml/datasets/bank+marketing)
📄 También disponible en Kaggle o con `seaborn` o `openml`.

**Descripción:**
Datos de una campaña de marketing telefónico de una entidad bancaria. El objetivo es predecir si un cliente contratará (`y` = "yes"/"no") un depósito a plazo.

---

### 🧩 Tareas detalladas

#### 1. **Carga y revisión inicial**

* Cargar el CSV con `pandas` o `polars`.
* Revisar tipos de datos, número de columnas, nulos, valores únicos.

#### 2. **EDA completo**

* Distribución de la variable objetivo (`y`) y análisis de balance.
* Análisis univariado:

  * Histogramas / countplots para variables numéricas y categóricas.
* Análisis bivariado:

  * Boxplots, violinplots, barplots para ver relaciones con `y`.
  * Mapa de calor de correlación para variables numéricas (`seaborn.heatmap`).
* Detección de valores atípicos (z-score o IQR si procede).
* Conclusiones intermedias: ¿Qué variables parecen relevantes?

#### 3. **Limpieza y transformación**

* Conversión de `y`: `"yes"` → `1`, `"no"` → `0`.
* Eliminar columnas redundantes si es justificable (como `duration`).
* Revisar y tratar nulos (si los hubiera).
* Crear nuevas variables si es útil.

#### 4. **Codificación de variables categóricas**

* One-Hot Encoding para variables nominales.
* Ordinal Encoding si alguna variable tiene orden lógico.
* Justificar cada elección.

#### 5. **Escalado de variables numéricas**

* Aplicar `StandardScaler`, `MinMaxScaler` o `RobustScaler` si el modelo lo requiere.
* Justificar si escalan y qué columnas lo necesitan.

#### 6. **División del dataset**

* Separar en `X` (features) e `y` (target).
* Usar `train_test_split` con `stratify=y` y `test_size=0.2`.

#### 7. **Entrenamiento inicial de modelos**

* Entrenar al menos 3 modelos diferentes:

  * Ej: `LogisticRegression`, `RandomForestClassifier`, `KNeighborsClassifier`, `SVC`, `XGBClassifier`
* Evaluar con métricas:

  * `accuracy`, `precision`, `recall`, `f1`, `ROC AUC`
* Mostrar matriz de confusión y curva ROC.

#### 8. **Selección del mejor modelo**

* Comparar resultados y justificar cuál se adapta mejor según las métricas y el objetivo.
* Escoger el mejor para optimizarlo.

#### 9. **Optimización de hiperparámetros**

* Aplicar `GridSearchCV` o `RandomizedSearchCV` sobre el modelo seleccionado.
* Mostrar los mejores parámetros obtenidos.
* Volver a evaluar el modelo optimizado.

#### 10. **Conclusiones finales**

* Comparar el rendimiento antes y después de la optimización.
* Reflexionar sobre qué variables influyeron más, qué modelo fue mejor y por qué.
* Entregar un resumen con los resultados y gráficos.

---

### 📦 Entregables

* 1 notebook completo con celdas Markdown explicativas + código.
* Archivo `.joblib` o `.parquet` con datos preparados (opcional).
* Gráficos generados durante el EDA y evaluación de modelos.
* Conclusión final bien redactada.

---

### 📊 Evaluación (rúbrica)

| Criterio                           | Peso |
| ---------------------------------- | ---- |
| Análisis exploratorio completo     | 25%  |
| Preprocesamiento y codificación    | 15%  |
| Entrenamiento y evaluación inicial | 20%  |
| Optimización y modelo final        | 20%  |
| Presentación y justificación final | 20%  |

---
¡Buena suerte y disfruta del proceso de ciencia de datos completo! 🚀