SELECT
    id AS movie_id,
    title,
    original_title,
    original_language,
    release_date,
    release_year,
    adult
FROM {{ ref('movies') }}