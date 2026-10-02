import json
from pathlib import Path
from movie_dw.db import get_connection

arquivos = list(Path("data/bronze/movies").rglob("movie_*.json"))
campos_obrigatorios = {"id", "title", "original_title", "release_date", "popularity", "vote_average", "vote_count", "adult", "original_language"}

print("Arquivos encontrados:", len(arquivos))

connection = get_connection()
cursor = connection.cursor()

carregados = 0
ignorados = 0

for arquivo in arquivos:
    with open(arquivo, encoding="utf-8") as f:
        filme = json.load(f)

    if not campos_obrigatorios.issubset(filme.keys()):
        ignorados += 1
        print("Ignorado:", arquivo)
        continue

    cursor.execute(
        """
        INSERT INTO staging.movies (id, title, original_title, release_date, popularity, vote_average, vote_count, adult, original_language)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
        """,
        (filme["id"], filme["title"], filme["original_title"], filme["release_date"] or None, filme["popularity"], filme["vote_average"], filme["vote_count"], filme["adult"], filme["original_language"])
    )

    carregados += cursor.rowcount

connection.commit()
cursor.close()
connection.close()

print("Inseridos:", carregados)
print("Ignorados:", ignorados)
print("Carga da staging finalizada!")