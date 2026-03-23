import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env desde el directorio del proyecto
env_file = Path(__file__).parent / ".env"
load_dotenv(env_file)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")