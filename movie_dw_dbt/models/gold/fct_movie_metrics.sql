SELECT
    id AS movie_id,
    popularity,
    vote_average,
    vote_count
FROM {{ ref('movies') }}