import pandas as pd 
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
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

    query_with_copy(query_str)
        For large queries, avoids the overhead from pandas built-in 'read_sql' function.

    insert(df)
        Inserts columns into the database table. 
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
            SQL query to execute. 

        Returns
        -------
        pd.Dataframe
            Result of the SQL query in the form of a pandas dataframe. 
        '''

        try:
            with tempfile.TemporaryFile() as tmp:
                query_sql = f'COPY ({query_str}) TO STDOUT WITH CSV HEADER'
                conn = self.engine.raw_connection() 
                cursor = conn.cursor() 
                cursor.copy_expert(query_sql, tmp)
                tmp.seek(0)
                df = pd.read_csv(tmp)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close() 
        return df 

    def insert(self, df: pd.DataFrame, cols: dict) -> str:
        ''' For inserting new data columns into the database table. There is no 
        built in way to insert new columns into an existing table. This methods 
        incorporates a work around where we create a temp table with the new columns
        and primary key and then merge it back into our shot_data_table.  

        Parameters
        ----------
        df : pd.DataFrame
            The data to be inserted into the table. MUST include id primary key column.
        
        cols : dict
            The columns to be added to the table. Formatted {column name: column type}
        
        Returns
        -------
        str
            Execution status. 
        '''

        # raise an error if the primary key is not included         
        if 'id' not in df:
            raise Exception("Data to be inserted must include 'id' (primary key) column.")

        # check the dictionary input isn't empty 
        if not cols:
            return 'No new columns provided'

        # write new dataframe to a temp table 
        df.to_sql('temp_table', self.engine, if_exists = 'replace', index = False, method = 'multi')

        # SQL commands
        column_commands = [f'ALTER TABLE shot_data_table ADD COLUMN {key} {val.upper()}' for key, val in cols.items()] 

        update_cols = [f'{key} = temp_table.{key}' for key in cols.keys()]
        update_sql = f"UPDATE shot_data_table SET {', '.join(update_cols)} FROM temp_table WHERE shot_data_table.id = temp_table.id"
        
        drop_sql = 'DROP TABLE temp_table'

        # execute commands 
        try:
            with self.engine.connect() as connection: 
                for com in column_commands:
                    connection.execute(text(com))
                connection.execute(text(update_sql))
                connection.execute(text(drop_sql))
                connection.commit()
        except SQLAlchemyError as e:
            print(f'SQLAlchemyError: {e}') 
            raise
        except Exception as ex:
            print(f'Error: {ex}')
            raise
        
        return 'Successful update'
