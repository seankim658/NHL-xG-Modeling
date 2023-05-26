import pandas as pd 
import numpy as np 
from database_connection import DBConn

'''
This script calculates a couple supplementary statistics using the X and y shot coordinates. The first statistic calculated
is shot angle, the second statistic calculated is shot distance. The reference point is the coordinate (89, 0) because it is 
89 ft from the goal line to the red line for a regulation NHL rink (approximately half the rink). 

Shot angle is calculated using the arctangent based on the x/Y coordinates of the shot. TODO : adjustments based on blocked shots,
shots behind the goaline, etc. 
'''

TABLE = 'shot_data_table'

# database connection 
db = DBConn()

# get all the data from the shot table 
shot_data = db.query(f'SELECT * FROM {TABLE}')

