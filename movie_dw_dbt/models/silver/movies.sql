SELECT
    id,
    TRIM(title) AS title,
    TRIM(original_title) AS original_title,
    release_date,
    popularity,
    vote_average,
    vote_count,
    adult,
    LOWER(original_language) AS original_language
FROM {{ source('staging', 'movies') }}