import os
from Data import Create_db, Create_Tables, Insert_Data

while True:
    print('D for Database access.')
    print('U for User access.')
    print('Q for quit.')
    choice=input('Enter D or U or Q:')
    if choice in 'Dd':
        while True:
            print('C for create DB')
            print('T for Create Tables')
            print('I for Insert Tables.')
            print('B for Back to Main Menu.')
            choice=input('Enter C or T or I:')
            if choice in 'cC':
                DB=input('Enter the Database name to create:')
                Create_db.create_sqlite_database(DB)
            elif choice in 'Tt':
                DB=input('Enter the DB name to create tables:')
                Create_Tables.creating_tables(DB)
            elif choice in 'iI':
                db=input('Enter the DB name to insert data:')
                Insert_Data.insert_data_into_tables(db)
                
            elif choice in 'Bb':
                continue
            elif choice.lower() not in 'cti':
                print('Invalid input.')
                quit
    elif choice in 'uU':
        quit
    else:
        break



