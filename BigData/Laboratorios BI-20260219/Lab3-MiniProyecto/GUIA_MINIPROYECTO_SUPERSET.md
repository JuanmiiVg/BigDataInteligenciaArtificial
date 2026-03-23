# Guía rápida - MiniProyecto UD4 (Superset)

## Dataset elegido (válido por rúbrica)
- Tabla: `public.orders_flat`
- Filas: `22.579` (cumple mínimo 10.000)
- Rango temporal: `2024-06-01` a `2024-07-30`
- Columnas clave: `fecha`, `canal`, `sku`, `qty`, `price`, `cost`

## 1) Comprobar conexión en Superset
1. Ir a **Settings > Database Connections**.
2. Abrir `Postgres_BI_Metabase`.
3. Verificar que conecta y que ve `public.orders_flat`.

## 2) Crear dataset
1. Ir a **Data > Datasets > + Dataset**.
2. Database: `Postgres_BI_Metabase`.
3. Schema: `public`.
4. Table: `orders_flat`.

## 3) Definir métricas (en Explore)
- **Ingresos**: `SUM(qty * price)`
- **Margen**: `SUM(qty * (price - cost))`
- **Pedidos**: `COUNT(DISTINCT order_id)`

## 4) Crear gráficos obligatorios
### A. KPI principal
- Tipo: **Big Number / KPI**
- Métrica: `SUM(qty * price)`
- Time column: `fecha`

**Captura:** `capturas/01_kpi_principal.png`

### B. Serie temporal
- Tipo: **Time-series Line Chart**
- Time column: `fecha`
- Métrica: `SUM(qty * price)`
- Time grain: día

**Captura:** `capturas/02_serie_temporal.png`

### C. Comparación por categoría
- Tipo: **Bar Chart**
- Dimensión: `canal`
- Métrica: `SUM(qty * price)`
- Orden: Desc por métrica

**Captura:** `capturas/03_comparacion_categoria.png`

### D. Segmentación / filtrado
- Tipo: **Bar Chart** (Top SKU) o **Table**
- Dimensión: `sku`
- Métrica: `SUM(qty * (price - cost))`
- Limitar Top 10
- Añadir filtros (canal y fecha) en dashboard

**Captura:** `capturas/04_segmentacion.png`

## 5) Dashboard final
1. Crear dashboard `MiniProyecto_UD4_BI`.
2. Añadir los 4 gráficos.
3. Añadir filtros globales: `fecha` y `canal`.
4. Orden recomendado: KPI, serie temporal, categoría, segmentación.

**Captura:** `capturas/05_dashboard_completo.png`

## 6) Qué entregar
- `UD4_MiniProyecto_Entrega.md` completo.
- Carpeta `capturas` con las 5 imágenes.
- Exportar a PDF si te lo piden en clase.
