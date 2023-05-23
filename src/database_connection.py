import numpy as np 
import pandas as pd 
from sqlalchemy import create_engine

class DBConn: 
    ''' Class for the database connection. 

    Attributes
    ----------
    host : str
        Host for connection to the PostgreSQL database.
    user : str 
        User to connect to the database under. 
    port : int 
        Port to connect to the database through (set during the container setup command).
    db : str 
        Database to connect to. 
    password : str 
        Corresponding password to the user. 
    table : str 
        Table in the database to connect to. 

    Methods
    -------
    __init__(host, user, port, db, password, table)
        Constructor. 
    
    '''

    def __init__(self, host: str = 'localhost', user: str = 'db_user', port: int = 5438, db: str = 'shot_db', password: str = 'LetMeIn', table: str = 'shot_data_table') -> None:
        ''' Constructor. 

        Parameters
        ----------
        host : str 
            Host for connection to the PostgreSQL database (default value 'localhost').
        user : str 
            User to connect to the database under (default value 'db_user').
        port : int 
            Port to connect to the database through (set during the container setup command, default value 5438).
        db : str 
            Database to connect to (default value 'shot_db')
        password : str 
            Corresponding password to the user (default value 'LetMeIn').
        table : str 
            Table in the database to connect to (default value 'shot_data_table').
        '''
        self.host = host 
        self.user = user 
        self.port = port 
        self.db = db 
        self.password = password 
        self.table = table 