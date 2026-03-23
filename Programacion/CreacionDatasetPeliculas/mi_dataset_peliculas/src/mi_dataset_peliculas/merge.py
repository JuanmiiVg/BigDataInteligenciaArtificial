def merge_tmdb_omdb(tmdb_list, omdb_getter):
    """Fusiona datos de TMDB con OMDb"""
    result = []
    for movie in tmdb_list:
        title = movie.get('title', '')
        omdb = omdb_getter(title)
        
        if omdb.get('Response') == 'True':
            movie_data = {
                "title": title,
                "release_date": movie.get("release_date"),
                "vote_average": movie.get("vote_average"),
                "runtime": omdb.get("Runtime"),
                "director": omdb.get("Director"),
                "imdb_rating": omdb.get("imdbRating"),
                "plot": omdb.get("Plot"),
                "actors": omdb.get("Actors")
            }
            result.append(movie_data)
    
    return result
