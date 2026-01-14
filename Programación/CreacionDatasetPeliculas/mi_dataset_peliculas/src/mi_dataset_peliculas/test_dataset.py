#!/usr/bin/env python
"""Script de prueba con datos simulados"""
from pathlib import Path
import pandas as pd

def main():
    """Genera un dataset de prueba sin necesidad de claves API"""
    print("\n📊 Generando dataset de prueba...\n")
    
    # Datos de ejemplo
    data = [
        {
            "title": "The Shawshank Redemption",
            "release_date": "1994-09-23",
            "vote_average": 9.3,
            "runtime": "142 min",
            "director": "Frank Darabont",
            "imdb_rating": "9.3",
            "plot": "Two imprisoned men bond over a number of years...",
            "actors": "Tim Robbins, Morgan Freeman, Bob Gunton"
        },
        {
            "title": "The Godfather",
            "release_date": "1972-03-24",
            "vote_average": 9.2,
            "runtime": "175 min",
            "director": "Francis Ford Coppola",
            "imdb_rating": "9.2",
            "plot": "The aging patriarch of an organized crime dynasty...",
            "actors": "Marlon Brando, Al Pacino, James Caan"
        },
        {
            "title": "The Dark Knight",
            "release_date": "2008-07-18",
            "vote_average": 9.0,
            "runtime": "152 min",
            "director": "Christopher Nolan",
            "imdb_rating": "9.0",
            "plot": "When the menace known as the Joker wreaks havoc...",
            "actors": "Christian Bale, Heath Ledger, Aaron Eckhart"
        },
        {
            "title": "Pulp Fiction",
            "release_date": "1994-10-14",
            "vote_average": 8.9,
            "runtime": "154 min",
            "director": "Quentin Tarantino",
            "imdb_rating": "8.9",
            "plot": "The lives of two mob hitmen, a boxer, a gangster...",
            "actors": "John Travolta, Samuel L. Jackson, Uma Thurman"
        },
        {
            "title": "Forrest Gump",
            "release_date": "1994-07-06",
            "vote_average": 8.8,
            "runtime": "142 min",
            "director": "Robert Zemeckis",
            "imdb_rating": "8.8",
            "plot": "The presidencies of Kennedy and Johnson unfold...",
            "actors": "Tom Hanks, Sally Field, Gary Sinise"
        },
    ]
    
    Path("data").mkdir(exist_ok=True)
    df = pd.DataFrame(data)
    
    # Guardar
    df.to_csv("data/dataset_peliculas_test.csv", index=False)
    
    print("✅ Dataset de prueba generado:")
    print(f"   📁 Archivo: data/dataset_peliculas_test.csv")
    print(f"   🎬 Películas: {len(df)}")
    print("\n📋 Contenido:")
    print(df.to_string(index=False))
    print("\n✨ ¡Listo para usar! Ahora configura tus claves API en .env para obtener datos reales.\n")

if __name__ == "__main__":
    main()
