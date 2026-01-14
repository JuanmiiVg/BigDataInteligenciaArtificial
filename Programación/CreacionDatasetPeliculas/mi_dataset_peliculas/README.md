# 🎬 Dataset de Películas - TMDB + OMDb

Proyecto Poetry para construir un dataset combinado de películas usando las APIs de TMDB y OMDb.

## 📋 Requisitos

- Python 3.10+
- Poetry
- Claves de API (gratuitas):
  - [TMDB API](https://developer.themoviedb.org/settings/api)
  - [OMDb API](https://www.omdbapi.com/apikey.aspx)

## 🚀 Instalación Rápida

```bash
# 1. Instalar dependencias
poetry install

# 2. Configurar claves API
cp .env.example .env
# Edita .env y añade tus claves de API

# 3. Ejecutar
poetry run build-dataset
```

## 📁 Estructura

```
mi_dataset_peliculas/
├── data/                  # Salida: CSV y Parquet
├── src/mi_dataset_peliculas/
│   ├── tmdb.py           # Cliente TMDB
│   ├── omdb.py           # Cliente OMDb
│   ├── merge.py          # Fusión de datos
│   ├── config.py         # Configuración
│   └── build_dataset.py  # Script principal
├── .env                  # Variables de entorno
├── .env.example          # Template de .env
└── pyproject.toml        # Configuración Poetry
```

## 🔑 Configuración de Claves API

### TMDB API Key
1. Crea una cuenta en https://www.themoviedb.org/settings/account
2. Accede a https://developer.themoviedb.org/settings/api
3. Genera una API key
4. Cópiala en `.env` → `TMDB_API_KEY`

### OMDb API Key
1. Visita https://www.omdbapi.com/apikey.aspx
2. Elige el plan "Free" 
3. Completa la verificación de email
4. Cópiala en `.env` → `OMDB_API_KEY`

## 🎯 Uso

```bash
# Construir dataset
poetry run build-dataset

# Ejecutar con Python directamente
poetry run python -m mi_dataset_peliculas.build_dataset
```

## 📊 Salida

El script genera:
- `data/dataset_peliculas.csv` - Dataset en CSV con columnas:
  - title
  - release_date
  - vote_average
  - runtime
  - director
  - imdb_rating
  - plot
  - actors

## 🐛 Solución de Problemas

### Error: "API key no configurada"
→ Verifica que tienes un archivo `.env` con las claves correctas

### Error: "API key inválida"
→ Comprueba que tu API key funciona en el sitio web de la API

### Error: "Timeout"
→ Puede haber problemas de red o límites de rate. Espera e intenta de nuevo.

## 📚 Próximos Pasos

- [ ] Agregar paginación para más películas
- [ ] Filtrar por género o año
- [ ] Análisis de datos con pandas/seaborn
- [ ] Servir con FastAPI
- [ ] Añadir base de datos (PostgreSQL/MongoDB)

## 📝 Notas

- Respeta los límites de rate de las APIs
- Las claves API son personales, no las compartas
- El archivo `.env` está en `.gitignore`

---

Made with ❤️ for data lovers
