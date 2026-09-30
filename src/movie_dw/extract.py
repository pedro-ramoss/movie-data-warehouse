from movie_dw.tmdb_client import get_movie

import json
import uuid
from datetime import date, datetime, timezone
from pathlib import Path
from requests.exceptions import RequestException
from movie_dw.tmdb_client import get_movie, get_popular_movie_ids


def extract_movie(movie_id):
    filme = get_movie(movie_id)

    load_id = str(uuid.uuid4())
    data_atual = date.today().isoformat()

    pasta_carga = Path(
        f"data/bronze/movies/{data_atual}/{load_id}"
    )

    pasta_carga.mkdir(
        parents=True,
        exist_ok=True
    )

    arquivo_filme = pasta_carga / f"movie_{movie_id}.json"

    with open(arquivo_filme, "w", encoding="utf-8") as bronze:
        json.dump(filme, bronze, ensure_ascii=False, indent=2)

    metadata = {
        "load_id": load_id,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "movie_id": movie_id,
        "endpoint": f"/movie/{movie_id}"
    }

    arquivo_metadata = pasta_carga / "metadata.json"

    with open(arquivo_metadata, "w", encoding="utf-8") as arquivo:
        json.dump(metadata, arquivo,ensure_ascii=False, indent=2)

    return pasta_carga


def extract_movies(movie_ids):



    load_id = str(uuid.uuid4())
    data_atual = date.today().isoformat()

    pasta_carga = Path(
        f"data/bronze/movies/{data_atual}/{load_id}"
    )

    pasta_carga.mkdir(
        parents=True,
        exist_ok=True
    )

    successful_ids = []
    failed_ids = []

    for movie_id in movie_ids:
        try:
            filme = get_movie(movie_id)

            arquivo_filme = pasta_carga / f"movie_{movie_id}.json"

            with open(arquivo_filme, "w", encoding="utf-8") as bronze:
                json.dump(
                    filme,
                    bronze,
                    ensure_ascii=False,
                    indent=2
                )

            successful_ids.append(movie_id)

        except RequestException:
            failed_ids.append(movie_id)
            print(f"Erro ao extrair filme {movie_id}")

    metadata = {
        "load_id": load_id,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "total_requested": len(movie_ids),
        "total_success": len(successful_ids),
        "total_failed": len(failed_ids),
        "successful_ids": successful_ids,
        "failed_ids": failed_ids
    }

    arquivo_metadata = pasta_carga / "metadata.json"

    with open(arquivo_metadata, "w", encoding="utf-8") as arquivo:
        json.dump(
            metadata,
            arquivo,
            ensure_ascii=False,
            indent=2
        )

    return pasta_carga

if __name__ == "__main__":
    ids = get_popular_movie_ids(100)

    pasta = extract_movies(ids)

    print("Carga salva em:", pasta)

