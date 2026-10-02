import json
from requests.exceptions import RequestException
from movie_dw import extract


def test_extract_movies(monkeypatch, tmp_path):

    def fake_get_movie(movie_id):
        return {
            "id": movie_id,
            "title": "Filme Teste"
        }

    monkeypatch.setattr(
        extract,
        "get_movie",
        fake_get_movie
    )

    monkeypatch.chdir(tmp_path)

    pasta = extract.extract_movies([101, 102])

    assert (pasta / "movie_101.json").exists()
    assert (pasta / "movie_102.json").exists()
    assert (pasta / "metadata.json").exists()

    with open(pasta / "metadata.json", encoding="utf-8") as arquivo:
        metadata = json.load(arquivo)

    assert metadata["status"] == "SUCCESS"
    assert metadata["total_requested"] == 2
    assert metadata["total_success"] == 2
    assert metadata["total_failed"] == 0
    assert metadata["successful_ids"] == [101, 102]
    assert metadata["failed_ids"] == []


def test_extract_movies_partial_failure(monkeypatch, tmp_path):

    def fake_get_movie(movie_id):
        if movie_id == 102:
            raise RequestException("Erro fake")
        return {"id": movie_id, "title": "Filme Teste"}

    monkeypatch.setattr(extract, "get_movie", fake_get_movie)

    monkeypatch.chdir(tmp_path)
    
pasta = extract.extract_movies([101, 102])


assert (pasta / "movie_101.json").exists()
assert not (pasta / "movie_102.json").exists()
assert (pasta / "metadata.json").exists()

with open(pasta / "metadata.json", encoding="utf-8") as arquivo:
    metadata = json.load(arquivo)
    
assert metadata["status"] == "PARTIAL_SUCCESS"
assert metadata["total_requested"] == 2
assert metadata["total_success"] == 1
assert metadata["total_failed"] == 1
assert metadata["successful_ids"] == [101]
assert metadata["failed_ids"] == [102]