# NHL xG Modeling 

**Work in progress.**

The goal of this project is to create an expected goal model using NHL shot event data from the NHL API. 

## Data 

Past season data collected from [Hockey-Statistics](https://hockey-statistics.com/shot-data/). Live data collected using [Hockey-Scraper](https://github.com/HarryShomer/Hockey-Scraper).

## Installation and Setup

### Docker Setup

1. Install [Docker](https://docs.docker.com/get-docker/) on your machine. 
2. Clone this repository to your machine. 
3. Build the custom Docker image from the included Dockerfile. Fill in the `IMAGE NAME` and fill in `PATH/TO/DOCKERFILE` with the proper path to the Dockerfile.   
```bash
docker image build -t <IMAGE NAME> <PATH/TO/DOCKERFILE>
```

### Conda Setup

Create a `conda` environment using the `conda_environment.yml` file and activate the environment. 

```bash
conda env create -f <PATH/TO/conda_environment.yml>  
conda activate XG_ENV
```

### Database Usage 

#### Running the PostgreSQL Database 

Run the Docker image that was created. Give a name to the container using `<CONTANINER NAME>`, and specify which port you want to use when accessing the database.  

```bash
docker run --name <CONTAINER NAME> -p <PORT>:5432 -d <IMAGE NAME>
```  

The Dockerfile specifies the following defaults:
* Database: `shot_db` 
* Username: `db_user`
* Password: `LetMeIn`  

Once you have the Docker image and created the container, you can freely start and stop the container without having to recreate the container again using the following commands: 

```bash
docker start <CONTAINER NAME>
docker stop <CONTAINER NAME>
```

#### Database Fields
1. `id` - Unique row identifier (primary key for `shot_data_table`)
2. `game_id` - Game Id as assigned by the league. The first 4 digits identify the season of the game (ie. 2012 for the 2012/2013 season). The next 2 digits give the type of game (01 = preseason, 02 = regular season, 03 = postseason, 04 = all-star). The last 4 digits identifies the specific game number. 
3. `season` - Season the game was played in in the format of `%Y%Y` (ex. 20122013)
4. `game_date` - Date the game was played in format `%m%d$Y`
5. `game_period` - Period the event occurred in
6. `shot_event` - Event type (ie. SHOT, MISS, BLOCK)
7. `seconds_elapsed` - Seconds elapsed since the start of the period (0-1200)
8. `strength` - Player strength when event occurred (ie. 5x5, 4x5, 5x4, etc.)
9. `strength2` - String representation of player strength (ie. EV, PP, etc.)
10. `event_team` - Team that the event occurred for 
11. `away_team` - Away team 
12. `home_Team` - Home team 
13. `position` - Player position that initiated/created the event 
14. `shoots` - Player who created the event's shooting side (R or L)
15. `player1` - Player who initiated/created the event 
16. `player2` - Secondary player involved in the event (defender if event was a block, primary assister if event was a goal)
17. `player3` - Third player involved in the event (secondary assister)
18. `away_player1` - Away skater 1 on the ice when the event occurred
19. `away_player2` - Away skater 2 on the ice when the event occurred
20. `away_player3` - Away skater 3 on the ice when the event occurred
21. `away_player4` - Away player 4 on the ice when the event occurred (goaltender if on 3x5 PK)
22. `away_player5` - Away player 5 on the ice when the event occurred (goaltender if on 4x5 PK)
23. `away_player6` - Away player 6 on the ice when the event occurred (skater if empty net, goaltender if EV)
24. `home_player1` - Home skater 1 on the ice when the event occurred
25. `home_player2` - Home skater 2 on the ice when the event occurred
26. `home_player3` - Home skater 3 on the ice when the event occurred 
27. `home_player4` - Home skater 4 on the ice when the event occurred (goaltender if on 3x5 PK)
28. `home_player5` - Home skater 5 on the ice when the event occurred (goaltender if on 4x5 PK)
29. `home_player6` - Away player 6 on the ice when the event occurred (skater if empty net, goaltender if EV)
30. `away_players` - Number of away players on ice (including goaltender)
31. `home_players` - Number of home players on ice (including goaltender)
32. `away_score` - Away team score 
33. `home_score` - Home team score 
34. `away_goalie` - Away team goaltender (blank if net empty)
35. `home_goalie` - Home team goaltender (blank if net empty)
36. `home_coach` - Home team head coach 
37. `away_coach` - Away team head coach 
38. `event_zone` - Zone the event was initiated in (Offensive zone = Off, Neutral zone = Neu, Defensive zone = Def)
39. `X` - On-ice X coordinate that the event occured 
40. `y` - On-ice y coordinate that the event occurred
41. `is_home` - Team that created the event (0 if away team, 1 if home team)
42. `Goalie` - Defending goaltender (blank if net empty)
43. `catches` - Side the defending goaltender catches on 
44. `shot_type` - Type of shot (ie. Wrist, Tip-In, Slap, etc.)
45. `loc` - If the shot event has an origination location (for blocked shots, the location of the block is contained in `X`/`y`, not where the shot was taken from)
46. `corsi` - Shot attempt 
47. `fenwick` - Non-blocked shot attempt 
48. `shot` - Shot on goal 
49. `goal` - Whether shot resulted in a goal 
50. `empty_net` - Whether either of the nets was empty (not necessarily the net facing the shot)
51. `xG` - Hockey-Statistics computer xG value 

## Authors and Acknowledgments 

Author: Sean Kim  
Acknowledgment: [Lars Skytte](https://twitter.com/HockeySkytte)  
Acknowledgment: [HarryShomer](https://github.com/HarryShomer)