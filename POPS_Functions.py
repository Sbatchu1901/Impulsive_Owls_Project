import sqlite3
from datetime import datetime
from tabulate import tabulate
import pandas as pd
import datetime
from datetime import date

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
    try:
        print('   ')
        print('   ')
        print('List of Orders:')
        cursor.execute('SELECT * FROM customer_orders')
        rows = cursor.fetchall()
        headers=['Order ID', 'Order Date', 'Product Name', 'Quantity','Customer ID','Shipping Address','Status','Shipped','Remarks']
        print(tabulate(pd.DataFrame(rows, columns=headers),headers='keys',tablefmt='grid',showindex=False))
        if not rows:
         print('No  orders found.')
         return
    
    except sqlite3 as e:
        print('No orders found.')

    finally:
        if conn:
            conn.close()

def Open_orders():
    print('    ')
    print('    ')
    conn= sqlite3.connect('POPS.db')
    cursor= conn.cursor()
    try:
        print('List of Open orders:')
        cursor.execute("SELECT * FROM Customer_orders WHERE status = 'Open'")
        rows = cursor.fetchall()
        headers= ['Order ID', 'Order Date', 'Product Name', 'Quantity', 'Customer ID', 'Shipping Address', 'Status', 'shipped', 'Remarks']
        print(tabulate(pd.DataFrame(rows, columns=headers),headers='keys',tablefmt='grid',showindex=False))
        if not rows:
            print('No open orders found')
            return
    
    except sqlite3.Error as e:
        print()(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()


def Verify_stock():
    print('Verifying stock for open orders.....')
    conn = sqlite3.connect('POPS.db')
    cursor = conn.cursor()
    try:
        
        cursor.execute("SELECT OrderID, OrderDate, ProductName, Quantity FROM customer_orders WHERE Status = 'Open'")
        orders = cursor.fetchall()

        if not orders:
            print('No open orders found.')
            return

        sufficient_inventory = []
        insufficient_inventory = []

        for order in orders:
            order_id = order[0]
            product_name = order[2]
            required_quantity = order[3]

            cursor.execute("SELECT productStock FROM Inventory WHERE LOWER(ProductName) = LOWER(?)", (product_name,))
            stock = cursor.fetchone()

            if stock and stock[0] >= required_quantity:
                sufficient_inventory.append(order)
            else:
                insufficient_inventory.append(order)

        # Display results
        headers = ['Order ID', 'Order Date', 'Product Name', 'Quantity']

        print('Orders with Sufficient Stock:')
        if sufficient_inventory:
            print(tabulate(pd.DataFrame(sufficient_inventory, columns=headers), headers='keys', tablefmt='grid', showindex=False))
        else:
            print('No orders with sufficient Stock.')

        print('   ')
        print('Orders with Insufficient Stock:')
        if insufficient_inventory:
            print(tabulate(pd.DataFrame(insufficient_inventory, columns=headers), headers='keys', tablefmt='grid', showindex=False))
        else:
            print('No orders with insufficient Stock.')



    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()



def Schedule_and_UpdateStatus():
    conn = sqlite3.connect('POPS.db')
    cursor = conn.cursor()

    try:
        # Display Open Orders for reference
        print("Fetching all open orders...")
        cursor.execute("SELECT * FROM customer_orders WHERE Status = 'Open'")
        orders = cursor.fetchall()
        if not orders:
            print("No open orders available for scheduling.")
            return
        headers = ['Order ID', 'Order Date', 'Product Name', 'Quantity', 'Customer ID', 'Shipping Address', 'Status', 'Shipped', 'Remarks']
        print(tabulate(orders, headers=headers, tablefmt="grid"))
    
        
        while True:
            try:
                Order_Id = int(input("Enter Order ID to assign the job: "))
                cursor.execute("SELECT * FROM customer_orders WHERE OrderID = ? AND Status = 'Open'", (Order_Id,))
                order = cursor.fetchone()
                if not order:
                    print(f"No open order found with ID {Order_Id}. Please enter a valid Order ID.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numeric Order ID.")

        # Input and validate Start and End Dates
        while True:
            Start_Date = input("Enter Start Date (YYYY-MM-DD): ")
            End_Date = input("Enter End Date (YYYY-MM-DD): ")
            try:
                current_date = date.today()
                start_date = datetime.datetime.strptime(Start_Date, "%Y-%m-%d").date()
                end_date = datetime.datetime.strptime(End_Date, "%Y-%m-%d").date()
                if start_date > end_date:
                    print("Start date cannot be later than the end date. Please try again.")
                    continue
                if start_date < current_date:
                    print('Start date cannot be in the past. Please try again.')
                    continue
                break
            except ValueError:
                print("Invalid date format. Please enter dates in YYYY-MM-DD format.")

        
        cursor.execute(
            """INSERT INTO Schedule_Jobs (OrderID, Job_Start_Date, Job_End_Date)
               VALUES (?, ?, ?)""",
            (Order_Id, Start_Date, End_Date,)
        )
        conn.commit()

        # Update the order status in customer_orders
        cursor.execute("UPDATE customer_orders SET Status = 'In Production' WHERE OrderID = ?", (Order_Id,))
        conn.commit()

        print(f"Job successfully scheduled for Order ID {Order_Id} from {Start_Date} to {End_Date}.")
        print('Order is Updated to In Production')

        cursor.execute(" SELECT OrderID, OrderDate, ProductName, Status  FROM customer_orders WHERE Status= 'In Production'")
        Records = cursor.fetchall()
        if not Records:
            print("No open orders available for scheduling.")
            return
        headers = ['Order ID', 'Order Date', 'Product Name',  'Status']
        print(tabulate(Records, headers=headers, tablefmt="grid"))
        

    except sqlite3.Error as e:
        print(f"An error occurred while scheduling the job: {e}")
    finally:
        if conn:
            conn.close()




