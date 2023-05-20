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

'''bash
conda env create -f <PATH/TO/conda_environment.yml>
conda activate XG_ENV
'''

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
1. **Game Id** - Game Id as assigned by the league. The first 4 digits identify the season of the game (ie. 2012 for the 2012/2013 season). The next 2 digits give the type of game (01 = preseason, 02 = regular season, 03 = postseason, 04 = all-star). The last 4 digits identifies the specific game number. 
2. **Season** - Season the game was played in in the format of `%Y%Y` (ex. 20122013)
3. **Date** - Date the game was played in format `%m%d$Y`
4. **Period** - Period the event occurred in
5. **Event** - Event type (ie. SHOT, MISS, BLOCK)
6. **Seconds_Elapsed** - Seconds elapsed since last event
7. **Strength** - Player strength when event occurred (ie. 5x5, 4x5, 5x4, etc.)
8. **Strength2** - String representation of player strength (ie. EV, PP, etc.)
9. **Ev_Team** - Team that the event occurred for 
10. **Away_Team** - Away team 
11. **Home_Team** - Home team 
12. **Position** - Player position that initiated/created the event 
13. **Shoots** - Player who created the event's shooting side (R or L)
14. **Player1** - Player who initiated/created the event 
15. **Player2** - Secondary player involved in the event (defender if event was a block, primary assister if event was a goal)
16. **Player3** - Third player involved in the event (secondary assister)
17. **awayPlayer1** - Away skater 1 on the ice when the event occurred
18. **awayPlayer2** - Away skater 2 on the ice when the event occurred
19. **awayPlayer3** - Away skater 3 on the ice when the event occurred
20. **awayPlayer4** - Away player 4 on the ice when the event occurred (goaltender if on 3x5 PK)
21. **awayPlayer5** - Away player 5 on the ice when the event occurred (goaltender if on 4x5 PK)
22. **awayPlayer6** - Away player 6 on the ice when the event occurred (skater if empty net, goaltender if EV)
23. **homePlayer1** - Home skater 1 on the ice when the event occurred
24. **homePlayer2** - Home skater 2 on the ice when the event occurred
25. **homePlayer3** - Home skater 3 on the ice when the event occurred 
26. **homePlayer4** - Home skater 4 on the ice when the event occurred (goaltender if on 3x5 PK)
27. **homePlayer5** - Home skater 5 on the ice when the event occurred (goaltender if on 4x5 PK)
28. **homePlayer6** - Away player 6 on the ice when the event occurred (skater if empty net, goaltender if EV)
29. **Away_Players** - Number of away players on ice (including goaltender)
30. **Home_Players** - Number of home players on ice (including goaltender)
31. **Away_Score** - Away team score 
32. **Home_Score** - Home team score 
33. **Away_Goalie** - Away team goaltender (blank if net empty)
34. **Home_Goalie** - Home team goaltender (blank if net empty)
35. **Home_Coach** - Home team head coach 
36. **Away_Coach** - Away team head coach 
37. **Event_Zone** - Zone the event was initiated in (Offensive zone = Off, Neutral zone = Neu, Defensive zone = Def)
38. **X** - On-ice X coordinate that the event was initiated from 
39. **y** - On-ice y coordinate that the event was initiated from 
40. **is_home** - Team that created the event (0 if away team, 1 if home team)
41. **Goalie** - Defending goaltender (blank if net empty)
42. **Catches** - Side the defending goaltender catches on 
43. **Shot_type** - Type of shot (ie. Wrist, Tip-In, Slap, etc.)
44. **Location** - 
45. **Corsi** - Shot attempt 
46. **Fenwick** - Non-blocked shot attempt 
47. **Shot** - Shot on goal 
48. **Goal** - Whether shot resulted in a goal 
49. **Empty Net** - Whether the net was empty 
50. **xG** - Hockey-Statistics computer xG value 

## Authors and Acknowledgments 

Author: Sean Kim  
Acknowledgment: [Lars Skytte](https://twitter.com/HockeySkytte)  
Acknowledgment: [HarryShomer](https://github.com/HarryShomer)