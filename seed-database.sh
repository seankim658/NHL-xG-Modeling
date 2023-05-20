#! /bin/bash 

# wait for PostgreSQL server to become available 
until psql -h "localhost" -U "db_user" -c '\l'; do
    >&2 echo "Waiting for Postgres - sleeping"
    sleep 1
done 

>&2 echo "Postgres is up - executing..."  

# loop through all csv data files in /docker-entrypoint-initdb.d/data and import each into PostgreSQL
for filename in /docker-entrypoint-initdb.d/data/*.csv; do 
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c \
        "\COPY shot_data_table(
            game_id,
            season,
            game_date,
            game_period,
            shot_event,
            seconds_elapsed,
            strength,
            strength_2,
            event_team,
            away_team,
            home_team,
            position,
            shoots,
            player1,
            player2,
            player3,
            away_player1,
            away_player2,
            away_player3,
            away_player4,
            away_player5,
            away_player6,
            home_player1,
            home_player2,
            home_player3,
            home_player4,
            home_player5,
            home_player6,
            away_players,
            home_players,
            away_score,
            home_score,
            away_goalie,
            home_goalie,
            home_coach,
            away_coach,
            event_zone,
            X,
            y,
            is_home,
            goalie,
            catches,
            shot_type,
            loc,
            corsi,
            fenwick,
            shot,
            goal,
            empty_net,
            xG
        ) \ 
        FROM '$filename' \ 
        DELIMITER ',' \ 
        CSV HEADER;"
done 