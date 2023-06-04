import pandas as pd 
import numpy as np 
import math
from database_connection import DBConn

'''
This script calculates a couple supplementary data features and one-hot encodes some categorical features. 
Script only needs to be run once after initial setup. After calculating the new data columns, it adds the 
features to the PostgreSQL table. 

**NOTE**
Generally speaking, this script is very inneficient, especially the calc_other_stats method. Calculating the 
event angle and event distance isn't too bad because essentially two calculations are being performed for each 
row. The calc_other_stats method, on the other hand, performs significantly more operations, specifically string
operations, which are relatively expensive in terms of computational resources. Since this script is only run once,
I just accepted the lazy (but slow) method here (aka I let it run for awhile and did some errands), however, I have 
also included an SQL file (that I wrote after) to calculate these same data features. Calculating directly in SQL 
is much faster due to the elimination of large data transferring to the server, much better memory management, and 
more advanced query optimizations. 

Supplementary features (used in all models): 

    event_distance: 
        Distance from the net, at (89, 0), in feet. Calculated using euclidean distance. 

    event_angle:
        Angle of the event in degrees relative to the net. Calculated using the arctangent based on the adjusted x, y coordinates.

Note: all shots coordinates in the data were already adjusted to appear they were taken towards the right side of the ice.    

Converted categorical features: 

    For all models: 

        score_down_4
        score_down_3
        score_down_2
        score_down_1
        score_up_4
        score_up_3
        score_up_2
        score_up_1
        score_even
        wrist_shot
        deflected_shot
        tip_shot
        slap_shot
        backhand_shot
        snap_shot
        wrap_shot
    
    For even strength model: 

        state_5v5
        state_4v4
        state_3v3
    
    For man adgantage model: 

        state_5v4
        state_4v3
        state_5v3
        state_6v5
        state_6v4 
    
    For shorthanded model: 

        state_4v5
        state_3v4
        state_3v5

'''

### Initial database interaction

TABLE = 'shot_data_table'

# database connection 
db = DBConn()

# get all the data from the shot table 
shot_data = db.query_with_copy(f'SELECT * FROM {TABLE}')

# TESTING
# shot_data = db.query(f"SELECT * FROM {TABLE} WHERE shot_event != 'BLOCK' AND x < 0 LIMIT 50")
# shot_data = db.query(f"SELECT * FROM {TABLE}  ORDER BY id ASC LIMIT 20")

### Calculated statistics

def calc_supp_stats(row): 

    def calc_distance(row):
        row['event_distance'] = math.sqrt((89 - row['x'])**2 + row['y']**2)
        return row 

    def calc_angle(row):
        try:
            row['event_angle'] = math.atan(row['y'] / (89 - abs(row['x']))) * (180 / math.pi)
        except ZeroDivisionError as e: 
            row['event_angle'] = 0.0
        except Exception as ex:
            print(f'Error: {ex}')
            print(row)
        return row 

    row = calc_distance(row)
    row = calc_angle(row)

    return row

shot_data = shot_data.apply(calc_supp_stats, axis = 1)

supp_df = shot_data[['id', 'event_distance', 'event_angle']]

print('Insert distance and angle columns:')
print(db.insert(supp_df, {'event_distance': 'float', 'event_angle': 'float'}))

### converting categorical features

def calc_other_stats(row):

    def score_margins(row):
        
        row['score_down_4'] = 0
        row['score_down_3'] = 0
        row['score_down_2'] = 0
        row['score_down_1'] = 0
        row['score_up_4'] = 0
        row['score_up_3'] = 0
        row['score_up_2'] = 0
        row['score_up_1'] = 0
        row['score_even'] = 0

        # shooting team was home team
        if row['is_home'] == 1:
            score_state = row['home_score'] - row['away_score']
            if score_state <= -4:
                row['score_down_4'] = 1
            elif score_state == -3:
                row['score_down_3'] = 1
            elif score_state == -2:
                row['score_down_2'] = 1
            elif score_state == -1:
                row['score_down_1'] = 1
            elif score_state == 0:
                row['score_even'] = 1
            elif score_state == 1:
                row['score_up_1'] = 1
            elif score_state == 2:
                row['score_up_2'] = 1
            elif score_state == 3:
                row['score_up_3'] = 1
            elif score_state >= 4:
                row['score_up_4'] = 1
        # shooting team was the away team
        else:
            score_state = row['away_score'] - row['home_score']
            if score_state <= -4:
                row['score_down_4'] = 1
            elif score_state == -3:
                row['score_down_3'] = 1
            elif score_state == -2:
                row['score_down_2'] = 1
            elif score_state == -1:
                row['score_down_1'] = 1
            elif score_state == 0:
                row['score_even'] = 1
            elif score_state == 1:
                row['score_up_1'] = 1
            elif score_state == 2:
                row['score_up_2'] = 1
            elif score_state == 3:
                row['score_up_3'] = 1
            elif score_state >= 4:
                row['score_up_4'] = 1
        
        return row 

    def shot_type(row):

        row['wrist_shot'] = 0
        row['deflected_shot'] = 0
        row['tip_shot'] = 0
        row['slap_shot'] = 0
        row['backhand_shot'] = 0
        row['snap_shot'] = 0
        row['wrap_shot'] = 0
        row['null_shot'] = 0

        if not isinstance(row['shot_type'], str):
            row['null_shot'] = 1
            return row 
        
        shot = row['shot_type'].lower()

        if shot == 'wrist':
            row['wrist_shot'] = 1
        elif shot == 'deflected':
            row['deflected_shot'] = 1
        elif shot == 'tip-in':
            row['tip_shot'] = 1
        elif shot == 'slap':
            row['slap_shot'] = 1
        elif shot == 'backhand':
            row['backhand_shot'] = 1
        elif shot == 'snap':
            row['snap_shot'] = 1
        elif 'wrap-around':
            row['wrap_shot'] = 1

        return row 

    def game_state(row):

        row['state_5v5'] = 0
        row['state_4v4'] = 0
        row['state_3v3'] = 0
        row['state_5v4'] = 0
        row['state_4v3'] = 0
        row['state_5v3'] = 0
        row['state_6v5'] = 0
        row['state_6v4'] = 0
        row['state_4v5'] = 0
        row['state_3v4'] = 0
        row['state_3v5'] = 0

        strength = row['strength']

        if strength == '5x5':
            row['state_5v5'] = 1
        elif strength == '4x4':
            row['state_4v4'] = 1
        elif strength == '3x3':
            row['state_3v3'] = 1
        
        # shooting team was the home team
        if row['is_home'] == 1:
            if strength == '5x4':
                row['state_5v4'] = 1
            elif strength == '4x3':
                row['state_4v3'] = 1
            elif strength == '5x3':
                row['state_5v3'] = 1
            elif strength == '6x5':
                row['state_6v5'] = 1
            elif strength == '6x4':
                row['state_6v4'] = 1
            elif strength == '4x5':
                row['state_4v5'] = 1
            elif strength == '3x4':
                row['state_3v4'] = 1
            elif strength == '3x5':
                row['state_3v5'] = 1
        # shooting team was the away team 
        else:
            if strength == '4x5':
                row['state_5v4'] = 1
            elif strength == '3x4':
                row['state_4v3'] = 1
            elif strength == '3x5':
                row['state_5v3'] = 1
            elif strength == '5x6':
                row['state_6v5'] = 1
            elif strength == '4x6':
                row['state_6v4'] = 1
            elif strength == '5x4':
                row['state_4v5'] = 1
            elif strength == '4x3':
                row['state_3v4'] = 1
            elif strength == '5x3':
                row['state_3v5'] = 1
        
        return row 

    row = score_margins(row)
    row = shot_type(row)
    row = game_state(row)

    return row 

shot_data = shot_data.apply(calc_other_stats, axis = 1)

cat_cols = ['id', 'score_down_4', 'score_down_3', 'score_down_2', 'score_down_1', 'score_up_4', 'score_up_3',
            'score_up_2', 'score_up_1', 'score_even', 'wrist_shot', 'deflected_shot', 'tip_shot', 'slap_shot',
            'backhand_shot', 'snap_shot', 'wrap_shot', 'null_shot', 'state_5v5', 'state_4v4', 'state_3v3', 'state_5v4',
            'state_4v3', 'state_5v3', 'state_6v5', 'state_6v4', 'state_4v5', 'state_3v4', 'state_3v5']

supp_df2 = shot_data[cat_cols]

cat_col_dict = {}
for col in cat_cols:
    if col != 'id':
        cat_col_dict[col] = 'int'

print('Insert converted categorical columns:')
print(db.insert(supp_df2, cat_col_dict))