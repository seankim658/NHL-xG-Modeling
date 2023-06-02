import pandas as pd 
import numpy as np 
import math
from database_connection import DBConn

'''
This script calculates a couple supplementary data features and one-hot encodes some categorical features.  

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
    
    For powerplay model: 

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

# testing
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

print('Insert distance and angle columns: ')
print(db.insert(supp_df, {'event_distance': 'float', 'event_angle': 'float'}))

### converting categorical features
