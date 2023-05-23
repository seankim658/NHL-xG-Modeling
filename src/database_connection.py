import numpy as np 
import pandas as pd 
from sqlalchemy import create_engine
from sqlalchemy import text 

class DBConn: 
    ''' Class for the database connection. 

    Attributes
    ----------
    _connection_string : str 
        Connection string for sqlalchemy. 
    engine : sqlalchemy.engine.Engine 
        Provides the database connectivity. 
    table : str 
        Table to query from. 

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
    
        self._connection_string = f'postgresql://{user}:{password}@{host}:{port}/{db}'
        self.engine = create_engine(self._connection_string)
        self.table = table 

    