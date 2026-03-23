---
title: "Errores comunes y checklist rápido de Altair"
author: "Curso de Especialización en Inteligencia Artificial y Big Data"
subtitle: "Programación de Inteligencia Artificial — Semana 04"
date: "2025-11-04"
geometry: margin=2cm
output: pdf_document
fontsize: 11pt
---

# 🧩 Errores comunes y checklist rápido de Altair

Altair es una librería declarativa para crear gráficos estadísticos de forma sencilla y expresiva.  
Esta lámina resume **los errores más comunes** y un **checklist rápido** para crear visualizaciones efectivas durante el EDA.

---

## 🧠 1️⃣ Errores comunes en Altair

| Tipo | Error típico | Cómo solucionarlo |
|------|---------------|-------------------|
| **Datos** | `MaxRowsError: The number of rows...` | Ejecuta `alt.data_transformers.disable_max_rows()` |
| **Tipos** | Ejes vacíos o mal agregados | Añade sufijo de tipo: `:Q` (numérico), `:N` (categórico), `:T` (fecha) |
| **Transformaciones** | Uso incorrecto de `.query()` o `.groupby()` | Usa `transform_filter`, `transform_aggregate`, `transform_bin` |
| **Interactividad** | Selección no filtra nada | Revisa `add_params(selection)` y `transform_filter(selection)` |
| **Escalas** | Rango de ejes incorrecto | Usa `scale=alt.Scale(zero=False, domain=[min,max])` |
| **Tooltips** | No se muestran valores | Añade `tooltip=['col1','col2']` |
| **Colores** | Exceso o mala asignación | Usa `scale=alt.Scale(scheme='category10')` |
| **Exportación** | Error al guardar PNG | Guarda `.html` o instala `altair_saver` + `selenium` |

---

## ✅ 2️⃣ Checklist rápido de Altair

### 🪄 Estructura básica
```python
chart = (
    alt.Chart(df)
       .mark_point()
       .encode(x='X:Q', y='Y:Q', color='Categoria:N', tooltip=['X','Y'])
)
chart
```

### 🎯 Escalas y ejes
```python
alt.X('X:Q', scale=alt.Scale(zero=False), title='Mi eje X')
alt.Y('Y:Q', scale=alt.Scale(domain=[10,50]))
```

### 🔁 Transformaciones
```python
.transform_filter("datum.Origin == 'USA'")
.transform_aggregate(total='sum(Sales)', groupby=['Country'])
.transform_bin('binned', field='Income', bin=alt.Bin(maxbins=20))
```

### 🧩 Interactividad
```python
sel = alt.selection_point(fields=['Country'], bind='legend')
chart.add_params(sel).transform_filter(sel)
```

### 🧱 Facetas y composición
```python
chart.facet(column='Origin')
chart1 | chart2   # lado a lado
chart1 + chart2   # superposición
```

### 💾 Guardar
```python
chart.save('grafico.html')
```

---

## 🧩 3️⃣ Buenas prácticas para enseñar y usar Altair

- ✔ Empieza siempre con `Chart → mark → encode`, y añade transformaciones después.  
- 💬 Usa títulos narrativos: cada gráfico debe responder una pregunta del EDA.  
- 🎨 No uses más de **3 canales visuales simultáneos** (color, tamaño, forma).  
- 🔍 Pide a los alumnos que modifiquen campos `x` y `y` para descubrir correlaciones.  
- 🧠 Compara con **Seaborn**: Altair requiere menos código y añade interactividad.  
- 💾 Recuerda que `chart.save('plot.html')` funciona en todos los entornos.  

---

> 🧩 **Consejo docente:** imprime esta hoja y úsala como recordatorio rápido en las sesiones de EDA con Altair.
