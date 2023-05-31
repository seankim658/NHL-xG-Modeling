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

shot_distance: 
    Distance from the net, at (89, 0), in feet. Calculated using euclidean distance. 

shot_angle:
    Angle of the shot in degrees relative to the net. Calculated using the arctangent based on the adjusted x, y coordinates.
'''

TABLE = 'shot_data_table'

# database connection 
db = DBConn()

# get all the data from the shot table 
shot_data = db.query(f'SELECT * FROM {TABLE} LIMIT 20')

def calc_adjusted_coords(row): 
    pass 

def calc_distance(row):
    pass 

def calc_angle(row):
    initial_angle = math.atan(row['y'] / (89 - abs(row['X']))) * (180 / math.pi)

