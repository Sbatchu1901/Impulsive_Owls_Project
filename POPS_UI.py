import os
from Data import Create_db, Create_Tables, Insert_Data
import POPS_Functions

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
                break
            elif choice.lower() not in 'cti':
                print('Invalid input.')
                quit
    elif choice in 'uU':
        while True:
            print('C for Clerck Access.')
            print('W for Warehouse Manager Access.')
            choice=input('Enter your role for access:')
            if choice in 'cC':
                print('R for Registering the New Customer.')
                print('T for Take Order and keep status is open.')
                print('A for Assign Order to Sales Person.')
                Clerk_choice=input('Enter R or T or A  to perform action:')
                if Clerk_choice in 'rR':
                    POPS_Functions.Register_Customer()
                elif Clerk_choice in 'tT':
                    POPS_Functions.Customer_Order()
                elif Clerk_choice in 'aA':
                    POPS_Functions.Assigned_Orders()

            elif choice in 'wW':
                while True:
                    Read_Order=input('Enter (R) to read all the Orders:')
                    if Read_Order in 'rR':
                        POPS_Functions.warehouse_Manager()
                        break
                    else:
                        break
            break
                


    else:
        break



