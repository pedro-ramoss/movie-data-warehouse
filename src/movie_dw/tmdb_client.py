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

if __name__ == "__main__":
    filme = get_movie(550)

    print("ID:", filme["id"])
    print("Título:", filme["title"])
    print("Data:", filme["release_date"])