from sqlite3 import connect

#--------------------------------------- CLASS AND FUNCTIONS

class database_manager:
    def __init__(self):
        self.__file_name = ''
        self.__database = None
        self.__cursor = None
    
    def config_database(self, client_name:str) -> int:
        """
        initialize the database
        and return the first insertable record
        """
        self.__file_name = f'Data/{client_name}.db'
        self.__database = connect(self.__file_name)
        self.__cursor = self.__database.cursor()
        self.__cursor.execute("""
                CREATE TABLE IF NOT EXISTS Keys (
                KeyCode INTEGER PRIMARY KEY ,
                Key TEXT
                )
                """)
        self.__cursor.execute("""
                CREATE TABLE IF NOT EXISTS Files (
                FilePath TEXT UNIQUE
                )
                """)
        self.__cursor.execute("SELECT MAX(KeyCode) FROM Keys")
        code = self.__cursor.fetchone()[0]
        if code is None:
            code = 0
        self.__database.commit()
        return code+1
    
    def write_data(self, *, file_path:str, key:bytes, key_code:int):
        self.__cursor.execute("""
                INSERT OR IGNORE INTO Files (FilePath)
                VALUES (:FilePath)
                """, {'FilePath': file_path})
        self.__cursor.execute("""
                INSERT INTO Keys (KeyCode, Key)
                VALUES (:KeyCode, :Key)
                """, {'KeyCode': key_code, 'Key': key})
        
        self.__database.commit()
    
    def read_data(self, key_code:int) -> bytes:
        self.__cursor.execute("SELECT Key FROM Keys WHERE KeyCode = :KeyCode", {'KeyCode': key_code})
        key = self.__cursor.fetchone()
        if key is None:
            return None
        return key[0]
    
    def close_database(self):
        self.__cursor.close()
        self.__database.close()
