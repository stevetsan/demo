-- MYSQL 5.7
SELECT
    COUNT(DISTINCT uid) AS num_of_user
FROM
    piwik_track
WHERE
    DATE(time) BETWEEN '2017-04-02' AND '2017-04-08'
        AND uid IN (
        SELECT
            uid
        FROM
            piwik_track
        WHERE
            DATE(time) = '2017-04-01'
                AND event_name = "FIRST_INSTALL")