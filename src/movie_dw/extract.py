from movie_dw.tmdb_client import get_movie

import json

filme = get_movie(550)

with open("data/bronze/movie_550.json", "w") as bronze:
    json.dump(filme, bronze)