-- Top passers by player

SELECT
    p.player_name,
    t.team_name,
    COUNT(*) AS total_passes
FROM events e
JOIN players p
    ON e.player_id = p.player_id
JOIN teams t
    ON e.team_id = t.team_id
WHERE e.event_type = 'Pass'
GROUP BY
    p.player_name,
    t.team_name
ORDER BY total_passes DESC;


-- Team passing metrics

SELECT
    t.team_name,
    COUNT(*) AS total_passes,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN e.outcome = 'Complete' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS team_pass_completion_pct
FROM events e
JOIN teams t
    ON e.team_id = t.team_id
WHERE e.event_type = 'Pass'
GROUP BY t.team_name
ORDER BY total_passes DESC;


-- Player pass completion metrics

SELECT
    p.player_name,
    t.team_name,
    COUNT(*) AS total_passes,
    SUM(
        CASE
            WHEN e.outcome = 'Complete' THEN 1
            ELSE 0
        END
    ) AS completed_passes,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN e.outcome = 'Complete' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS pass_completion_pct
FROM events e
JOIN players p
    ON e.player_id = p.player_id
JOIN teams t
    ON e.team_id = t.team_id
WHERE e.event_type = 'Pass'
GROUP BY
    p.player_name,
    t.team_name
HAVING COUNT(*) > 20
ORDER BY total_passes DESC;