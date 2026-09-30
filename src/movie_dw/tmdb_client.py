import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("TMDB_API_TOKEN")

headers = {
    "Authorization": f"Bearer {api_key}"
}   

def get_movie(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    
    resposta = requests.get(
        url,
        headers=headers,
        timeout=10)

    resposta.raise_for_status()

    return resposta.json()

def get_popular_movies(page=1):
    url = "https://api.themoviedb.org/3/movie/popular"

    params = {
        "page": page
    }

    resposta = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    resposta.raise_for_status()

    return resposta.json()

def get_popular_movie_ids(limit=100):
    ids = []
    page = 1

    while len(ids) < limit:
        dados = get_popular_movies(page)

        for filme in dados["results"]:
            ids.append(filme["id"])

            if len(ids) >= limit:
                break

        page += 1

    return ids