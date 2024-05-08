'''
Created on Feb 25, 2024

@author: Thomas
'''


import psycopg2


# Global variables
SERVER = ""
DATABASE = ""
USERNAME = ""
PASSWORD = ""


class DbUtils(object):
    '''
    classdocs
    '''


    def __init__(self, server, database, username, password):
        '''
        Constructor
        '''
        global SERVER
        global DATABASE
        global USERNAME
        global PASSWORD
        SERVER = server
        DATABASE = database
        USERNAME = username
        PASSWORD = password


    def getConnection(self):
        return psycopg2.connect(host=SERVER, port="5432",
            database=DATABASE,
            user=USERNAME,
            password=PASSWORD)


    def executeSQL(self, sql_str):
        try:
            dbConnection = self.getConnection()
            dbConnection.autocommit = True
            print("Connection ok")
            cursor = dbConnection.cursor()
            print("Executing SQL: '%s'..." % sql_str)
            cursor.execute(sql_str)
            if sql_str.startswith("SELECT") or sql_str.startswith("select"):
                return cursor.fetchall()
        except Exception as e:
            print("ERROR: %s" % (str(e)))
            raise Exception(str(e))
        finally:
            # closing database connection.
            if dbConnection:
                cursor.close()
                dbConnection.close()
                print("PostgreSQL connection is closed")


    def executeSQLs(self, sql_strs):
        try:
            dbConnection = self.getConnection()
            dbConnection.autocommit = True
            print("Connection ok")
            cursor = dbConnection.cursor()
            for sql_str in sql_strs:
                print("Executing SQL: '%s'..." % sql_str)
                cursor.execute(sql_str)
        except Exception as e:
            print("ERROR: %s" % (str(e)))
            raise Exception(str(e))
        finally:
            # closing database connection.
            if dbConnection:
                cursor.close()
                dbConnection.close()
                print("PostgreSQL connection is closed")


