CREATE VIEW GAMES_BY_USER AS
SELECT
    g.id,
    g.title,
    g.maker,
    g.game_type_id,
    g.number_of_players,
    g.skill_level,
    u.id user_id,
    u.first_name || ' ' || u.last_name AS full_name
FROM
    levelupapi_game g
JOIN
    levelupapi_gamer gr ON g.gamer_id = gr.id
JOIN
    auth_user u ON gr.user_id = u.id


CREATE VIEW EVENTS_BY_USER AS
SELECT 
    au.id AS gamer_id,
    au.first_name || " " || au.last_name AS full_name,
    e.id AS event_id,
    e.date AS event_date,
    e.time as event_time,
    gm.title as game_name
FROM levelupapi_gamer AS gr
JOIN auth_user AS au 
    ON au.id = gr.user_id
JOIN levelupapi_event_attendees AS ea
    ON ea.gamer_id = au.id
JOIN levelupapi_event AS e
    on ea.event_id = e.id
JOIN levelupapi_game as gm
    ON e.game_id = gm.id