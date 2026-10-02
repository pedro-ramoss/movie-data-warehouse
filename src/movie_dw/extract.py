import json
import uuid
from datetime import date, datetime, timezone
from pathlib import Path
from requests.exceptions import RequestException
from movie_dw.tmdb_client import get_movie, get_popular_movie_ids

def extract_movies(movie_ids):
    load_id = str(uuid.uuid4())
    data_atual = date.today().isoformat()

    pasta_carga = Path(f"data/bronze/movies/{data_atual}/{load_id}")

    pasta_carga.mkdir(parents=True, exist_ok=True)

    successful_ids = []
    failed_ids = []

    arquivo_metadata = pasta_carga / "metadata.json"

    metadata = {
        "load_id": load_id,
        "status": "RUNNING",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "finished_at": None,
        "total_requested": len(movie_ids),
        "total_success": 0,
        "total_failed": 0,
        "successful_ids": [],
        "failed_ids": []
    }

    with open(arquivo_metadata, "w", encoding="utf-8") as arquivo:
        json.dump(metadata, arquivo, ensure_ascii=False, indent=2)

    try:
        for movie_id in movie_ids:
            try:
                filme = get_movie(movie_id)
                arquivo_filme = pasta_carga / f"movie_{movie_id}.json"

                with open(arquivo_filme, "w", encoding="utf-8") as bronze:
                    json.dump(filme, bronze, ensure_ascii=False, indent=2)

                successful_ids.append(movie_id)

            except RequestException:
                failed_ids.append(movie_id)
                print(f"Erro ao extrair filme {movie_id}")

        metadata["status"] = "PARTIAL_SUCCESS" if failed_ids else "SUCCESS"

    except KeyboardInterrupt:
        metadata["status"] = "INTERRUPTED"                  
        raise

    except Exception:
        metadata["status"] = "FAILED"
        raise

    finally:
        metadata["finished_at"] = datetime.now(timezone.utc).isoformat()
        metadata["total_success"] = len(successful_ids)
        metadata["total_failed"] = len(failed_ids)
        metadata["successful_ids"] = successful_ids
        metadata["failed_ids"] = failed_ids

        with open(arquivo_metadata, "w", encoding="utf-8") as arquivo:
            json.dump(metadata, arquivo, ensure_ascii=False, indent=2)

    return pasta_carga

if __name__ == "__main__":
    movie_ids = get_popular_movie_ids(10)
    pasta = extract_movies(movie_ids)


