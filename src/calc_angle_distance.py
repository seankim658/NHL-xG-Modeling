import pandas as pd 
import numpy as np 
import math
from database_connection import DBConn

'''
This script calculates a couple supplementary data features: 

event_distance: 
    Distance from the net, at (89, 0), in feet. Calculated using euclidean distance. 

event_angle:
    Angle of the event in degrees relative to the net. Calculated using the arctangent based on the adjusted x, y coordinates.

Note: all shots coordinates in the data were already adjusted to appear they were taken towards the right side of the ice.    
'''

TABLE = 'shot_data_table'

# database connection 
db = DBConn()

# get all the data from the shot table 
# testing
# shot_data = db.query(f"SELECT * FROM {TABLE} WHERE shot_event != 'BLOCK' AND x < 0 LIMIT 50")
shot_data = db.query(f"SELECT * FROM {TABLE} WHERE shot_event != 'BLOCK' LIMIT 500")

def calc_supp_stats(row): 

    def calc_distance(row):
        row['event_distance'] = math.sqrt((89 - row['x'])**2 + row['y']**2)
        return row 

    def calc_angle(row):
        row['event_angle'] = math.atan(row['y'] / (89 - abs(row['x']))) * (180 / math.pi)
        return row 

    row = calc_distance(row)
    row = calc_angle(row)

    return row

shot_data = shot_data.apply(calc_supp_stats, axis = 1)
shot_data.to_csv('test.csv')