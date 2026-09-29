import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("TMDB_API_TOKEN")
   


url = "https://api.themoviedb.org/3/movie/550"

headers = {
    "Authorization": f"Bearer {api_key}"
}

resposta = requests.get(url, headers=headers, timeout=10)

print(resposta.status_code)

dados = resposta.json()


print("ID:", dados["id"])
print("Título:", dados["title"])
print("Data de lançamento:", dados["release_date"])