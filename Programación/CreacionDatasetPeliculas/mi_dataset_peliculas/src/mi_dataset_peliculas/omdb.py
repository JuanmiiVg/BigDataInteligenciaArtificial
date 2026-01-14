import requests
from .config import OMDB_API_KEY

def get_omdb_data(title):
    if not OMDB_API_KEY:
        raise ValueError(
            "❌ API key de OMDb no configurada. "
            "Actualiza el archivo .env con tu clave de https://www.omdbapi.com/apikey.aspx"
        )
    
    params = {
        "apikey": OMDB_API_KEY,
        "t": title,
        "type": "movie"
    }
    try:
        resp = requests.get("http://www.omdbapi.com/", params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error obteniendo datos de OMDb para '{title}': {e}")
        return {"Response": "False"}
