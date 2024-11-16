import sqlite3
from datetime import date
from tabulate import tabulate
import pandas as pd

def Register_Customer():
    try:
        print('------------------')
        Customer_Name=input('Customer Name:')
        print('------------------')
        Customer_Phone=input('Customer Phone:')
        print('------------------')
        Customer_Email=input('Customer Email:')
        
        conn= sqlite3.connect('POPS.db')

        cursor = conn.cursor()

        cursor.execute('INSERT INTO customer (CustomerName, CustomerPhone, CustomerEmail) VALUES (?,?,?)',
                       (Customer_Name,Customer_Phone,Customer_Email))
        conn.commit()
        

        cursor.execute('SELECT CustomerID from customer ORDER BY CustomerID DESC LIMIT 1')
        Customer_ID = cursor.fetchone()[0]
        print('-------------------------------------------------------------')
        print(f"{Customer_Name} Registered Successfully! ID is {Customer_ID}.")
        print('-------------------------------------------------------------')
    except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        
    finally:
            if conn:
                conn.close()
    

def Customer_Order():
    try:
        conn= sqlite3.connect('POPS.db')
        cursor = conn.cursor()
        cursor.execute('SELECT ProductName FROM Inventory')
        rows = cursor.fetchall()
        headers=['MENU']

        print(tabulate(rows, headers=headers, tablefmt="grid"))

        print('------------------')
        Product_Name=input('Product Name:')
        print('------------------')
        Order_Quantity=input('Order Quantity:')
        print('------------------')
        CustomerID=input('Customer ID:')
        print('------------------')
        Shipping_Address=input('Shipping Address:')
        Status='Open'
        Shipped='No'
        Order_Date=date.today()
        print('------------------')
        Remarks=input('Any remarks:')

        cursor.execute("""INSERT INTO customer_orders(OrderDate, ProductName, Quantity, CustomerID, ShippingAddress, Status, Shipped, Remarks) 
                       VALUES (?,?,?,?,?,?,?,?)""",
                       (Order_Date,Product_Name,Order_Quantity,CustomerID,Shipping_Address,Status,Shipped,Remarks))
        conn.commit()
        

        cursor.execute('SELECT OrderID from customer_orders ORDER BY OrderID DESC LIMIT 1')
        Order_ID = cursor.fetchone()[0]
        cursor.execute('SELECT CustomerID from customer_orders where OrderID=?',(Order_ID,))
        Cust_ID=cursor.fetchone()[0]
        cursor.execute('SELECT CustomerName from customer where CustomerID =?',(Cust_ID,))
        Cust_Name=cursor.fetchone()[0]
        print('-------------------------------------------------------------')
        print(f"{Cust_Name} order is successfully placed. Order ID is {Order_ID}.")
        print('-------------------------------------------------------------')
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        
    finally:
        if conn:
            conn.close()

def Assigned_Orders():
    while True:
        try:
            conn= sqlite3.connect('POPS.db')
            cursor = conn.cursor()
            print('   ')
            print('   ')
            print('List of Orders:')
            cursor.execute('SELECT * FROM customer_orders where Status=?',('Open',))
            rows = cursor.fetchall()
            headers=['Order ID', 'Order Date', 'Product Name', 'Quantity','Customer ID','Shipping Address','Status','Shipped','Remarks']

            print(tabulate(pd.DataFrame(rows, columns=headers),headers='keys',tablefmt='grid',showindex=False))
            print('  ')
            print('  ')
            print('List of Sales Persons:')
            cursor.execute('SELECT * FROM SalesPersons')
            rows = cursor.fetchall()
            headers=['Sales Person ID',  'Sales Person Name', 'Sales Person Contact','Sales Person Email']

            print(tabulate(pd.DataFrame(rows, columns=headers),headers='keys',tablefmt='grid',showindex=False))
            print('   ')
            print('   ')

            OrderIs=input('Order ID is:')
            
            cursor.execute('SELECT OrderID from customer_orders where OrderID=?',(OrderIs,))
            Order_ID = cursor.fetchone()
            if Order_ID is not None and int(Order_ID[0]) == int(OrderIs):
                AssignedTo=input('Assigned to sales person ID:')
                cursor.execute('SELECT SalesPersonID from SalesPersons where SalesPersonID=?',(AssignedTo,))
                salespersonID = cursor.fetchone()
                if salespersonID is not None and int(salespersonID[0]) == int(AssignedTo):
                    cursor.execute("""INSERT INTO Assigned_Orders (OrderID, SalesPersonID) VALUES (?,?)""",
                                (OrderIs,AssignedTo))
                    conn.commit()
                    print('-----------------------------------------')
                    print(f'Order {OrderIs} is successfully assigned to {AssignedTo}')
                    print('-----------------------------------------')
                    break
                else:
                    print('-----------------------------------------')
                    print(f'Provided sales person ID {AssignedTo}  is not in our records.\n Please check and try again.')
                    print('-----------------------------------------')
                    continue
            else:
                print('-----------------------------------------')
                print(f'Provided Order ID {OrderIs} is not in our records.\n Please check and try again.')
                print('-----------------------------------------')
                continue

        except sqlite3.Error as e:
                print(f"An error occurred: {e}")
                
        finally:
            if conn:
                conn.close()


def warehouse_Manager():
    print('  ')
    print('  ')
    conn= sqlite3.connect('POPS.db')
    cursor = conn.cursor()
    print('   ')
    print('   ')
    print('List of Orders:')
    cursor.execute('SELECT * FROM customer_orders')
    rows = cursor.fetchall()
    headers=['Order ID', 'Order Date', 'Product Name', 'Quantity','Customer ID','Shipping Address','Status','Shipped','Remarks']
    print(tabulate(pd.DataFrame(rows, columns=headers),headers='keys',tablefmt='grid',showindex=False))
