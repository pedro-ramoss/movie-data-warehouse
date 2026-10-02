SELECT
    id,
    TRIM(title) AS title,
    TRIM(original_title) AS original_title,
    release_date,
    EXTRACT(YEAR FROM release_date)::INTEGER AS release_year,
    popularity,
    CASE
        WHEN vote_average BETWEEN 0 AND 10 THEN vote_average
        ELSE NULL
    END AS vote_average,
    vote_count,
    adult,
    LOWER(original_language) AS original_language
FROM {{ source('staging', 'movies') }}