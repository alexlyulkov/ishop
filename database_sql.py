sql_types = {'int':'INTEGER', 'long':'INTEGER', 'str':'TEXT', 'unicode':'TEXT', 'float':'REAL'}

from employee import Employee
import sqlite3
import psycopg2
import database
import traceback

class database_sql(database.database):
    def __init__(self):
        self.db = None
        self.cursor = None
        self.f = None
        
    def init_sqlite(self, filename):
        self.f = '?'
        self.db = sqlite3.connect(filename, check_same_thread = False)
        self.init_tables()

    def init_postgresql(self, database, user, password, host, port):
        self.f = '%s'
        self.db = psycopg2.connect(database = database, user = user, password = password,
                                   host = host, port = port, async = 0)
        self.init_tables()
        
    def init_tables(self):
        self.cursor = self.db.cursor()

        columns = Employee().to_dict()
        del columns['id']

        request = 'CREATE TABLE IF NOT EXISTS employees '
        request += "(id INTEGER PRIMARY KEY UNIQUE"
        for column, value in columns.items():
            request += ', ' + column + ' ' + \
                           sql_types[type(value).__name__]
        request += ")"
        
        self.cursor.execute(request)
        self.db.commit()
        
    def save_user(self, user):
        pass

    def load_user(self, user_email):
        pass

    def save_product(self, product):

    def load_product(self, product_id):
        pass
