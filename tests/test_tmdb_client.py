from movie_dw.tmdb_client import get_popular_movie_ids
from movie_dw import tmdb_client


def test_get_popular_movie_ids():
    ids = get_popular_movie_ids(3)

    assert isinstance(ids, list)
    assert len(ids) == 3
    assert all(isinstance(movie_id, int) for movie_id in ids)

def test_get_popular_movie_ids_mock(monkeypatch):

    def fake_api(page=1):
        return {
            "results": [
                {"id": 101},
                {"id": 102},
                {"id": 103},
                {"id": 104}
            ]
        }

    monkeypatch.setattr(
        tmdb_client,
        "get_popular_movies",
        fake_api
    )

    ids = tmdb_client.get_popular_movie_ids(3)

    assert isinstance(ids, list)
    assert len(ids) == 3
    assert ids == [101, 102, 103]
    

