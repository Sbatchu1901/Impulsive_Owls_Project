import sqlite3
from datetime import date
from tabulate import tabulate

def Register_Customer():
    try:
        
        Customer_Name=input('Customer Name:')
        Customer_Phone=input('Customer Phone:')
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


        Product_Name=input('Product Name:')
        Order_Quantity=input('Order Quantity:')
        CustomerID=input('Customer ID:')
        Shipping_Address=input('Shipping Address:')
        Status='Open'
        Shipped='No'
        Order_Date=date.today()
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