import psycopg2

class DbUtils:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port="5432",
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Connection to PostgreSQL DB successful")
        except Exception as e:
            print(f"The error '{e}' occurred")

    def executeSQL(self, sql_str, values=None):
        try:
            cursor = self.connection.cursor()
            print(f"Executing SQL: '{sql_str}'...")
            cursor.execute(sql_str, values)
            if sql_str.strip().lower().startswith("select"):
                return cursor.fetchall()
            self.connection.commit()
        except Exception as e:
            print(f"ERROR: {e}")
            raise Exception(str(e))
        finally:
            cursor.close()

    def executeSQLs(self, sql_strs):
        try:
            cursor = self.connection.cursor()
            for sql_str in sql_strs:
                print(f"Executing SQL: '{sql_str}'...")
                cursor.execute(sql_str)
            self.connection.commit()
        except Exception as e:
            print(f"ERROR: {e}")
            raise Exception(str(e))
        finally:
            cursor.close()