# 🧪 Proyecto de Creación de Dataset Meteorológico

## 🌍 Introducción

Esta tarea consiste en construir un pequeño sistema de predicción de temperatura utilizando datos reales de meteorología. A partir de fuentes abiertas como **Open-Meteo**, **AEMET** u otras similares, extraerás datos atmosféricos como temperatura, humedad, viento, etc., los analizarás y entrenarás un modelo que permita predecir la temperatura a partir de algunas de estas variables.

Se trata de un proceso completo: desde la descarga y limpieza de los datos hasta su visualización, modelado y (si es posible) el despliegue del sistema como API. Esto simula un flujo real en proyectos de ciencia de datos o analítica predictiva.

---

## 🧠 ¿Qué aprenderás?

- Cómo automatizar la obtención de datos meteorológicos reales
- Cómo preparar esos datos para su análisis y modelado
- Qué significa **predecir** una variable numérica (regresión)
- Qué es un **modelo de aprendizaje automático** y cómo se entrena
- Cómo **guardar y reutilizar** un modelo entrenado
- Qué es una **API de predicción** y por qué es útil

---

## 🧪 Qué se espera que hagas

1. **Obtención de datos**: usando APIs como Open-Meteo, WeatherAPI, AEMET CSV, etc.
2. **Visualización exploratoria**: gráficas para observar la evolución de temperatura, correlaciones, etc.
3. **Preparación**: crear variables útiles como hora, día, eliminar errores, completar datos si es necesario.
4. **Modelado**: elegir y entrenar un modelo con al menos dos variables predictoras.
5. **Comparación**: repetir usando más variables, comparar resultados.
6. **Guardar modelo**: usa `joblib` para guardarlo como `modelo_entrenado.pkl`.
7. **Desplegar** (si puedes): expón una API `/predict` con FastAPI que reciba `humedad`, `viento`, etc. y devuelva la temperatura esperada.

---

## 📚 Recursos útiles

- Open-Meteo API: https://open-meteo.com/
- AEMET datos abiertos: https://datosclima.aemet.es/
- Pandas, seaborn, matplotlib para análisis y visualización
- Scikit-learn, cuML, XGBoost o LightGBM para modelos
- FastAPI y Uvicorn para servir el modelo

---

## ✍️ Recomendaciones

- Empieza con pocas variables (ej. humedad + viento) y entrena un modelo simple
- Evalúa con MSE, MAE o R2 para saber si el modelo funciona
- Si tienes GPU, prueba cuML
- Usa Git si quieres llevar registro del avance

---

¿Preparado para predecir el tiempo? ☁️🌡️

