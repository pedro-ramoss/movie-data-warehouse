SELECT
    release_year,
    COUNT(*) AS total_movies,
    AVG(vote_average) AS avg_vote_average,
    AVG(popularity) AS avg_popularity,
    SUM(vote_count) AS total_votes
FROM {{ ref('movies') }}
WHERE release_year IS NOT NULL
GROUP BY release_year
ORDER BY release_year