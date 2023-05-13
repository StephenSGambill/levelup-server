SELECT g.id, 
    g.title, g.maker, 
    g.skill_level, 
    g.number_of_players, 
    g.game_type_id,
    au.first_name ,
    au.last_name, g.gamer_id
FROM levelupapi_game AS g
JOIN levelupapi_gamer AS gm ON gm.id = g.gamer_id
JOIN auth_user AS au ON au.id = gm.user_id;
