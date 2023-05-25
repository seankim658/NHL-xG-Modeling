import numpy as np 
import pandas as pd 
from sqlalchemy import create_engine
from sqlalchemy import text 
import tempfile

class DBConn: 
    ''' Class for the database connection. 

    Attributes
    ----------
    _connection_string : str 
        Connection string for sqlalchemy. 
    engine : sqlalchemy.engine.Engine 
        Provides the database connectivity. 

    Methods
    -------
    __init__(host, user, port, db, password)
        Constructor. 
    
    query(query_str)
        Query a table in the database. 
    '''

    def __init__(self, host: str = 'localhost', user: str = 'db_user', port: int = 5438, db: str = 'shot_db', password: str = 'LetMeIn') -> None:
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

    def query(self, query_str: str) -> pd.DataFrame:
        ''' Query a table in the database using SQL. 

        Parameters
        ----------
        query_str : str 
            SQL query to execute. 

        Returns 
        -------
        pd.Dataframe 
            Result of the SQL query in the form of a pandas dataframe. 
        '''

        with self.engine.connect() as connection:
            result = connection.execute(text(query_str))
        # TODO
        df = pd.DataFrame(result.fetchall())

        return df
    
    def query_with_copy(self, query_str: str) -> pd.DataFrame:
        ''' For large queries such as SELECT * FROM [table].

        By using a temporary file to run a large query, we can 
        avoid some of the memory overhead and constraints from 
        pandas built-in 'read_sql' function. 

        Parameters
        ----------
        query_str : str
            SQL query to execute

        Returns
        -------
        pd.Dataframe
            Result of the SQL query in the form of a pandas dataframe. 
        '''

        # TODO 
        pass 


    