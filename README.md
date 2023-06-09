# NHL xG Modeling 

**Work in progress.**

The goal of this project is to create an expected goal model using NHL shot event data from the NHL API. 

- [Data](#data)
    - [Data Notes](#data-notes)
- [Installation and Setup](#installation-and-setup)
    - [Docker Setup](#docker-setup)
    - [Conda Setup](#conda-setup)
    - [Database Usage](#database-usage)
        - [Running the PostgreSQL Database](#running-the-postgresql-database)
        - [Database Fields](#database-fields)
        - [Calculated Database Fields](#calculated-database-fields)
- [Modeling](#modeling)
- [Future Work](#future-work)
- [Reference Image](#reference-image)
- [Authors and Acknowledgments](#authors-and-acknowledgments)

## Data 

Past season data collected from [Hockey-Statistics](https://hockey-statistics.com/shot-data/). Live data collected using [Hockey-Scraper](https://github.com/HarryShomer/Hockey-Scraper).

### Data Notes 
There are a few differences in the initial data versus the raw data gathered from the NHL PBP API data:
- For shot block events, the NHL PBP data has player1 as the blocker and player2 as the shooter. This has been switched around in the hockey-statistics data, player1 is the shooter and player2 is the blocker.  
- For shot block events, the NHL PBP data has the event zone correspond to the defensive (blocking team). In the NHL data, the event_zone would be the defensive zone. Since player1 is the shooter in the hockey-statistics data, the event_zone is the offensive zone.  
- In the hockey-statistics data, (x, y) coordinates are preprocessed to make it appear as if all shots were taken on the right side of the ice. This was done to standardize the data in order to calculate all events in relation to the net reference point, in this case (89, 0). The only coordinates that were not changed are those that are marked as occurring in the defensive zone. 

Another data piece to note is that especially in earlier season data, there are more goals and shots marked as being scored from the defensive zone, there are a couple potential reasons for this. Some are simply mistakes by NHL trackers and should have been marked as occurring in the offensive zone. Other times, incomplete passes or attempted ices that end up on net are counted as a shot on net, because it would have gone in if not for the "save". 

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

Run the Docker image that was created. Give a name to the container using `<CONTANINER NAME>`, and specify which port (scripts assume port 5438 was used) you want to use when accessing the database.  

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
39. `x` - On-ice X coordinate that the event occured (coordinates were preprocessed to appear as if they were taken towards the right end of the ice, meaning the x coordinate is usually positive except for some shots listed as taken explicitly from the defensive zone) 
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
51. `xG` - Hockey-Statistics computed xG value 

#### Calculated Database Fields

These supplementary data fields can be calculated using the `features_calc.sql` file. The relevant data records can be isolated into separate tables using the `create_supplementary_tables.sql` file. 

52. `event_distance` - Distance in feet from the net that the event occurred 
53. `event_angle` - Angle in relation to the net that the event occurred
54. `score_down_4` - Whether the team taking the shot was down 4 or more at the time 
55. `score_down_3` - Whether the team taking the shot was down 3 at the time 
56. `score_down_2` - Whether the team taking the shot was down 2 at the time
57. `score_down_1` - Whether the team taking the shot was down 1 at the time 
58. `score_up_4` - Whether the team taking the shot was up 4 or more at the time 
59. `score_up_3` - Whether the team taking the shot was up 3 at the time
60. `score_up_2` - Whether the team taking the shot was up 2 at the time 
61. `score_up_1` - Whether the team taking the shot was up 1 at the time
62. `score_even` - Whether the score was tied at the time of the shot event
63. `wrist_shot` - Whether the shot type was a wrist shot
64. `deflected_shot` - Whether the shot type was a deflected shot 
65. `tip_shot` - Whether the shot type was a tip 
66. `slap_shot` - Whether the shot type was a slap shot
67. `backhand_shot` - Whether the shot type was a backhand shot 
68. `snap_shot` - Whether the shot type was a snap shot 
69. `wrap_shot` - Whether the shot type was a wrap-around
70. `null_shot` - Whether the shot type was missing  
71. `state_5v5` - Whether the teams were playing at 5 on 5 (used for the even strength model)
72. `state_4v4` - Whether the teams were playing at 4 on 4 (used for the even strength model)
73. `state_3v3` - Whether the teams were playing at 3 on 3 (used for the even strength model)
74. `state_5v4` - Whether the team taking the shot was playing 5 on 4 (used for the man advantage model)
75. `state_4v3` - Whether the team taking the shot was playing 4 on 3 (used for the man advantage model)
76. `state_5v3` - Whether the team taking the shot was playing 5 on 3 (used for the man advantage model)
77. `state_6v5` - Whether the team taking the shot was playing 6 on 5 (used for the man advantage model)
78. `state_6v4` - Whether the team taking the shot was playing 6 on 4 (used for the man advantage model)
79. `state_4v5` - Whether the team taking the shot was playing 4 on 5 (used for the shorthanded model)
80. `state_3v4` - Whether the team taking the shot was playing 3 on 4 (used for the shorthanded model)
81. `state_3v5` - Whether the team taking the shot was playing 3 on 5 (used for the shorthanded model)
82. `is_forward` - Whether the player taking the shot was a forward 
83. `off_wing` - Whether the player taking the shot was on his off or strong side of the ice 

## Modeling 

Features used during modeling:  

| Continuous Features | Discrete Features (Dummy Variables) |
|---------------------|-------------------------------------|
| event_distance      | is_home                             |
| event_angle         | score_down_4                        |            
| seconds_elapsed     | score_down_3                        | 
| game_period         | score_down_2                        |
| x                   | score_down_1                        |
| y                   | score_up_4                          |
|                     | score_up_3                          |
|                     | score_up_2                          |
|                     | score_up_1                          |
|                     | score_even                          |
|                     | wrist_shot                          |
|                     | deflected_shot                      |
|                     | tip_shot                            |
|                     | slap_shot                           |
|                     | backhand_shot                       |
|                     | snap_shot                           |
|                     | wrap_shot                           |                        
|                     | state_5v5*                          |
|                     | state_4v4*                          | 
|                     | state_3v3*                          |
|                     | state_5v4^                          |
|                     | state_4v3^                          |
|                     | state_5v3^                          | 
|                     | state_6v5^                          |
|                     | state_6v4^                          |
|                     | state_4v5+                          |
|                     | state_3v4+                          | 
|                     | state_3v5+                          |
|                     | is_forward                          |
|                     | off_wing                            |

\* only used in even strength model  
^ only used in man advantage model   
\+ only used in short handed model  

## Future Work 

Section in progress.

## Reference Image

![rink](imgs/NHL_rink.jpg)

## Authors and Acknowledgments 

Author: Sean Kim  
Acknowledgment: [Lars Skytte](https://twitter.com/HockeySkytte)  
Acknowledgment: [HarryShomer](https://github.com/HarryShomer)