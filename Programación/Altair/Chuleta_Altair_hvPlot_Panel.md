---
title: "Chuleta rápida — Altair · hvPlot · Panel"
author: "Curso de Especialización en Inteligencia Artificial y Big Data"
subtitle: "Programación de Inteligencia Artificial — Semana 04"
date: "2025-11-03"
geometry: margin=2cm
output: pdf_document
fontsize: 11pt
---

# 🧠 Chuleta rápida: Altair · hvPlot · Panel

> Curso: **Programación de Inteligencia Artificial — Semana 04**  
> Tema: *Visualización avanzada e interactiva con Altair, hvPlot y Panel*  
> Dataset: *Online Retail II (UCI)*  

---

## 🎨 ALTair — Visualización declarativa

📚 **Documentación:** [https://altair-viz.github.io/](https://altair-viz.github.io/)

### 🧩 Concepto clave
Altair usa una *gramática de gráficos declarativa*: describes **qué quieres ver**, no **cómo dibujarlo**.

### 🔹 Estructura general

```python
import altair as alt

chart = (alt.Chart(df)
    .mark_bar()
    .encode(
        x='VariableX:Q',
        y='VariableY:Q',
        color='Categoría:N',
        tooltip=['VariableX','VariableY']
    )
)
chart
```

**Tipos de dato:**  
`:Q` (numérico) · `:N` (categórico) · `:O` (ordinal) · `:T` (temporal)

---

### 🔹 Histogramas y agregaciones

```python
alt.Chart(df).mark_bar().encode(
    x=alt.X('Total:Q', bin=alt.Bin(maxbins=50)),
    y='count()'
).interactive()
```

### 🔹 Barras agregadas (Top N)

```python
alt.Chart(df).transform_aggregate(
    total_sum='sum(Total)', groupby=['Description']
).transform_window(
    rank='rank()', sort=[alt.SortField('total_sum', order='descending')]
).transform_filter('datum.rank <= 10'
).mark_bar().encode(
    x='total_sum:Q', y=alt.Y('Description:N', sort='-x')
)
```

### 🔹 Gráfico interactivo (selector)

```python
selector = alt.selection_point(fields=['Country'], bind='legend')
alt.Chart(df.sample(20000)).mark_circle(size=60, opacity=0.5).encode(
    x='UnitPrice:Q', y='Quantity:Q', color='Country:N', size='Total:Q',
    tooltip=['Country','UnitPrice','Quantity','Total']
).add_params(selector).transform_filter(selector).interactive()
```

🧭 *Más sobre selecciones avanzadas:*  
[https://altair-viz.github.io/user_guide/interactions.html](https://altair-viz.github.io/user_guide/interactions.html)

---

## ⚡ hvPlot — Visualización interactiva simple

📚 **Documentación:** [https://hvplot.holoviz.org/](https://hvplot.holoviz.org/)

### 🧩 Concepto clave
hvPlot permite crear **gráficos interactivos** directamente desde un DataFrame Pandas/cuDF.

### 🔹 Ejemplos básicos

```python
import hvplot.pandas
df.hvplot.scatter(x='UnitPrice', y='Quantity', color='Country', alpha=0.5)
df.hvplot.barh(y='Total', x='Country', title='Top países')
df.hvplot.line(x='Date', y=['Total','MA7'], title='Ventas diarias')
```

### 🔹 Opciones comunes

```python
.opts(width=600, height=300, legend_position='top_left')
```

🧭 *Más ejemplos y tipos de gráfico:*  
[https://hvplot.holoviz.org/user_guide/Introduction.html](https://hvplot.holoviz.org/user_guide/Introduction.html)

---

## 🧭 Panel — Dashboards interactivos ligeros

📚 **Documentación:** [https://panel.holoviz.org/](https://panel.holoviz.org/)

### 🧩 Estructura general

```python
import panel as pn
pn.extension()

selector = pn.widgets.Select(name='Country', options=['ALL','Spain','UK'], value='ALL')

@pn.depends(selector)
def grafico(country):
    df_sel = df if country == 'ALL' else df[df['Country'] == country]
    return df_sel.hvplot.barh(x='Description', y='Total', title=f'Top productos ({country})')

dashboard = pn.Column(selector, grafico)
dashboard
```

### 🔹 Composición visual

```python
pn.Row(grafico1, grafico2)
pn.Column(widget, grafico1)
pn.Tabs(('Ventas', grafico1), ('Países', grafico2))
```

### 🔹 Exportar a HTML

```python
dashboard.save('dashboard_ventas.html')
```

🧭 *Más sobre layouts y templates:*  
[https://panel.holoviz.org/user_guide/index.html](https://panel.holoviz.org/user_guide/index.html)

---

## 🧩 Comparativa práctica

| Criterio | Altair | hvPlot | Panel |
|-----------|--------|--------|--------|
| Filosofía | Declarativo | Simple desde DataFrames | Dashboards |
| Sintaxis | `mark_*`, `encode` | `df.hvplot.*()` | `@pn.depends` |
| Interactividad | Alta | Automática | Completa |
| Ideal para | Storytelling | EDA rápido | Dashboards |
| Exportable | SVG, HTML | HTML | HTML |
| Base | Vega-Lite | Bokeh/Holoviews | Bokeh/Holoviews |

---

## 🧠 Resumen visual

```
[ DataFrame Pandas/cuDF ]
        │
        ├──► Altair → storytelling narrativo
        ├──► hvPlot → exploración rápida
        └──► Panel  → dashboards ligeros
```

---

## 🔗 Enlaces de referencia

- [Altair User Guide](https://altair-viz.github.io/user_guide/)
- [hvPlot Introduction](https://hvplot.holoviz.org/)
- [Panel User Guide](https://panel.holoviz.org/)
- [Holoviz Ecosystem Overview](https://holoviz.org/)
- [Altair Gallery](https://altair-viz.github.io/gallery/index.html)
- [Vega-Lite Reference](https://vega.github.io/vega-lite/)
