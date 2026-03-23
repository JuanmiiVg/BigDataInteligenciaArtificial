# 📦 Entrega – Proyecto de Predicción Meteorológica

## 1. Datos del grupo

- Alumno/a 1: Juan Manuel Vega
- Alumno/a 2: —
- Curso: Big Data
- Fecha de entrega: 22 de enero de 2026

---

## 2. Objetivo del proyecto

- **Variable a predecir**: Temperatura (temperature_2m en °C)
- **Utilidad del modelo**: Predecir la temperatura a partir de variables meteorológicas como humedad relativa y velocidad del viento. Útil para aplicaciones de alertas climáticas, sistemas de climatización automática o planificación agrícola.
- **Datos de entrada**: Humedad relativa (%) y velocidad del viento (m/s)

---

## 3. Fuentes de datos utilizadas

- **Servicio utilizado**: Open-Meteo API (https://open-meteo.com/) - datos meteorológicos históricos
- **Formato**: JSON (desde API), convertido a CSV y Parquet
- **Fusión de fuentes**: Se intentó fusionar con AEMET pero no se disponía de archivo local. Se utilizó únicamente Open-Meteo.
- **Ubicación**: Sevilla (37.39°N, -5.99°O)
- **Período**: 1 al 10 de septiembre de 2023 (datos horarios)

---

## 4. Visualizaciones y exploración

- **Gráficos utilizados**: 
  - Gráfico de líneas temporal de temperatura (10 días × 24 horas = 240 puntos)
  - Gráfico de líneas temporal de humedad relativa (240 puntos)
- **Relaciones observadas**:
  - La temperatura fluctúa entre 17°C y 34°C en el período analizado
  - Se observa un patrón de variación diaria clara (máximos durante el día, mínimos en la noche)
  - La humedad relativa muestra una relación inversa: alta cuando la temperatura es baja, baja cuando es alta
  - La velocidad del viento varía entre 0 y 10 m/s aproximadamente
- **Variables seleccionadas**: Se decidió usar humedad relativa y velocidad del viento como predictores porque muestran correlación visible con los cambios de temperatura

---

## 5. Preparación de los datos

- **Columnas disponibles**: 
  - `time`: timestamp en formato datetime (extraído de la API)
  - `temperature_2m`: temperatura a 2m de altura (°C)
  - `relative_humidity_2m`: humedad relativa (%)
  - `wind_speed_10m`: velocidad del viento a 10m de altura (m/s)
- **Transformaciones realizadas**: Conversión de time a datetime con `pd.to_datetime()` y ajuste de timezone a Europe/Madrid
- **Escalado/normalización**: Aún no se ha aplicado (previsto en fase de modelado)
- **Construcción X e y**: 
  - X: `[relative_humidity_2m, wind_speed_10m]`
  - y: `temperature_2m`
- **Tamaño del dataset**: 240 registros horarios (10 días × 24 horas)

---

## 6. Entrenamiento del modelo

- **Modelos probados**: (En desarrollo) Se prevé probar:
  - Linear Regression (línea base)
  - Random Forest Regressor
  - Gradient Boosting (XGBoost o LightGBM)
- **Librerías utilizadas**: scikit-learn (versión 1.7.2)
- **Métricas de evaluación**: 
  - Mean Squared Error (MSE)
  - Mean Absolute Error (MAE)
  - R² Score
- **División del dataset**: 80% entrenamiento, 20% validación
- **Comparación de variables**: Se evaluará el modelo con 2 variables (humedad + viento) vs. con más variables si se fusionan otras fuentes de datos

---

## 7. Guardado y uso del modelo

- **Formato de guardado del dataset**: 
  - CSV: `dataset_meteo.csv` (legible, compatible con Excel)
  - Parquet: `dataset_meteo.parquet` (comprimido, optimizado para análisis)
- **Modelo entrenado**: Se guardará con `joblib` como `modelo_temperatura.pkl` una vez completado el entrenamiento
- **Usos posteriores del modelo**:
  - Sistema de alerta temprana de temperaturas extremas
  - Integración en aplicaciones móviles de predicción meteorológica
  - Automatización de sistemas de climatización
  - Análisis de tendencias climáticas locales
  - Base para modelos más complejos con más variables (presión, radiación solar, etc.)

---

## 8. API de predicción (si se ha hecho)

- **Estado**: En desarrollo
- **Framework**: FastAPI + Uvicorn
- **Endpoint previsto**: `POST /predict`
- **Datos de entrada esperados**: JSON con campos `humedad` (%) y `viento` (m/s)
- **Salida esperada**: JSON con `temperatura_predicha` (°C) y confianza del modelo
- **Ejemplo de request**:
  ```json
  {
    "humedad": 65,
    "viento": 3.5
  }
  ```
- **Ejemplo de response**:
  ```json
  {
    "temperatura_predicha": 24.5,
    "confianza": 0.87
  }
  ```

---

## 9. Reflexión final

- **Parte más desafiante**: La integración de múltiples fuentes de datos y la alineación temporal (fusión por timestamp). También el manejo de APIs externas y sus limitaciones.
- **Aprendizajes clave**:
  - Los datos reales siempre requieren más limpieza y preparación de lo esperado
  - La visualización temprana es clave para identificar relaciones entre variables
  - Las APIs públicas son herramientas poderosas para obtener datos sin necesidad de costosas subscripciones
  - Un modelo simple con pocas variables puede dar buenos resultados si se seleccionan bien
- **Mejoras futuras**:
  - Ampliar el período de datos (históricos más largos para mejor generalización)
  - Agregar más variables meteorológicas (presión atmosférica, radiación solar, etc.)
  - Incluir efectos temporales (hora del día, día de la semana) como features
  - Comparar múltiples modelos sistemáticamente
  - Automatizar la descarga diaria de datos para reentrenamiento
  - Desplegar la API en la nube (Azure, AWS, etc.)

---

## 10. Evidencias del trabajo

Adjunta al menos tres:
- ☑ El notebook relleno y ejecutado: `Lab_EDA_Meteo_OpenMeteo_AEMET.ipynb`
- ☑ Visualización generada: Gráfico de temperatura horaria (1-10 sept 2023)
- ☑ Visualización generada: Gráfico de humedad relativa horaria (1-10 sept 2023)
- ☑ Dataset guardado: `dataset_meteo.csv` (240 registros × 4 columnas)
- ☑ Dataset guardado: `dataset_meteo.parquet` (formato optimizado)
- ⏳ Resultado de entrenamiento: En desarrollo (fase siguiente)
- ⏳ Captura del endpoint de la API: En desarrollo (fase siguiente)

---