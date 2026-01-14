from pathlib import Path
import pandas as pd
from .tmdb import get_popular_movies
from .omdb import get_omdb_data
from .merge import merge_tmdb_omdb


from pathlib import Path
import pandas as pd
from .tmdb import get_popular_movies, get_total_movies
from .omdb import get_omdb_data
from .merge import merge_tmdb_omdb


def main():
    """Construye y guarda el dataset de películas"""
    try:
        Path("data").mkdir(exist_ok=True)
        
        # Calcular número de páginas
        total_movies = get_total_movies()
        total_pages = (total_movies + 9) // 10  # Redondear hacia arriba
        
        print(f"📥 Obteniendo {total_movies} películas ({total_pages} páginas)...\n")
        
        all_merged_data = []
        
        # Obtener películas de cada página
        for page in range(1, total_pages + 1):
            print(f"📄 Página {page}/{total_pages}...", end=" ", flush=True)
            tmdb_movies = get_popular_movies(page=page)
            
            if not tmdb_movies:
                print("(no más películas)")
                break
            
            print(f"({len(tmdb_movies)} películas) 🔗", end=" ", flush=True)
            merged_data = merge_tmdb_omdb(tmdb_movies, get_omdb_data)
            all_merged_data.extend(merged_data)
            print(f"✅ ({len(merged_data)} encontradas)\n", flush=True)
        
        if all_merged_data:
            df = pd.DataFrame(all_merged_data)
            df.to_csv("data/dataset_peliculas.csv", index=False)
            print(f"\n{'='*60}")
            print(f"✅ Dataset guardado correctamente")
            print(f"   📁 Archivo: data/dataset_peliculas.csv")
            print(f"   🎬 Total de películas: {len(df)}")
            print(f"   📊 Columnas: {', '.join(df.columns.tolist())}")
            print(f"{'='*60}\n")
            
            print("🎞️  Primeras películas:")
            print(df[['title', 'director', 'imdb_rating']].head(10).to_string(index=False))
            print()
        else:
            print("\n⚠️ No se encontraron películas válidas.")
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        raise


if __name__ == "__main__":
    main()
