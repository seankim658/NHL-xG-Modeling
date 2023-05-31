import pandas as pd 
import numpy as np 
import math
from database_connection import DBConn

'''
This script calculates a few supplementary data features: 

adjusted_x: 
    Adjusts the shot x coordinate so the shot always appears as if it were at the right end of the rink. 

adjusted_y: 
    Adjusts the shot y coordinate so the shot always appears as if it were at the right end of the rink. 

event_distance: 
    Distance from the net, at (89, 0), in feet. Calculated using euclidean distance. 

event_angle:
    Angle of the event in degrees relative to the net. Calculated using the arctangent based on the adjusted x, y coordinates.
'''

TABLE = 'shot_data_table'

# database connection 
db = DBConn()

# get all the data from the shot table 
shot_data = db.query(f'SELECT * FROM {TABLE} LIMIT 20')

def calc_adjusted_coords(row): 
    if row['X'] < 0.0:
        row['adjusted_X'] = abs(row['X'])
        row['adjusted_y'] = -row['y']
    else:
        row['adjusted_X'] = row['X']
        row['adjusted_y'] = row['y']
    return row 

def calc_distance(row):
    row['event_distance'] = math.sqrt((89 - row['adjusted_X'])**2 + row['adjusted_y']**2)
    return row 

def calc_angle(row):
    row['event_angle'] = math.atan(row['adjusted_y'] / (89 - abs(row['adjusted_X']))) * (180 / math.pi)
    return row 

