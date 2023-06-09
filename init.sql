CREATE TABLE IF NOT EXISTS shot_data_table (
    id SERIAL PRIMARY KEY,
    game_id INT,
    season INT, 
    game_date DATE,
    game_period SMALLINT,
    shot_event VARCHAR,
    seconds_elapsed INT,
    strength VARCHAR,
    strength_2 VARCHAR,
    event_team VARCHAR,
    away_team VARCHAR,
    home_team VARCHAR,
    position VARCHAR,
    shoots VARCHAR,
    player1 VARCHAR,
    player2 VARCHAR,
    player3 VARCHAR, 
    away_player1 VARCHAR,
    away_player2 VARCHAR,
    away_player3 VARCHAR,
    away_player4 VARCHAR,
    away_player5 VARCHAR, 
    away_player6 VARCHAR,
    home_player1 VARCHAR,
    home_player2 VARCHAR,
    home_player3 VARCHAR,
    home_player4 VARCHAR,
    home_player5 VARCHAR,
    home_player6 VARCHAR,
    away_players SMALLINT, 
    home_players SMALLINT,
    away_score SMALLINT,
    home_score SMALLINT, 
    away_goalie VARCHAR,
    home_goalie VARCHAR,
    home_coach VARCHAR,
    away_coach VARCHAR,
    event_zone VARCHAR,
    X SMALLINT,
    y SMALLINT,
    is_home SMALLINT,
    goalie VARCHAR,
    catches VARCHAR,
    shot_type VARCHAR,
    loc SMALLINT,
    corsi SMALLINT,
    fenwick SMALLINT,
    shot SMALLINT,
    goal SMALLINT,
    empty_net SMALLINT,
    xG FLOAT
);