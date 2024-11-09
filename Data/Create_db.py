import sqlite3
import os

from Data import Create_Tables

def create_sqlite_database(filename):

    if os.path.exists(filename):
        print('DB is already exists')
    else:

        """ create a database connection to an SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(filename)
        except sqlite3.Error as e:
            print(e)
        else:
            print(f'Created the {filename} database file.')
            Insert=input(f'Do you want to insert data in {filename} database (yes/no)?')
            if Insert.lower() in 'yes':
                Create_Tables.creating_tables(filename)
            else:
                quit
        finally:
            if conn:
                conn.close()