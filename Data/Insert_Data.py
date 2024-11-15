import sqlite3

def insert_data_into_tables(db):
    print('In which table do you want to insert?')
    print('=====================================')
    print('Enter I for Inventory Table.')
    print('Enter S for Sales Person Table.')
    choice=input('Enter I or S:')

    if choice in 'iI':
        try:
            
            product_Name=input('Enter product name:')
            product_stock=input('Enter the stock of product:')
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Inventory (ProductName, productStock) VALUES (?, ?)'
                , (product_Name,product_stock))
            conn.commit()
            print("Data inserted successfully into inventory table.")
        
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        
        finally:
            if conn:
                conn.close()
    elif choice in "sS":
        try:
            
            SalesPerson_Name=input('Enter sales person name:')
            SalesPerson_Contact=input('Enter sales person contact:')
            SalesPerson_Email=input('Enter sales person Email ID:')
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO SalesPersons (SalesPersonName, SalesPersonContact,SalesPersonEmail)
                VALUES (?, ?,?)
                 ''', (SalesPerson_Name,SalesPerson_Contact,SalesPerson_Email))
            conn.commit()
            print("Data inserted successfully into Sales persons table.")
        
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        
        finally:
            if conn:
                conn.close()
    else:
        quit

