import sqlite3
from datetime import datetime
from tabulate import tabulate
import pandas as pd
import datetime
from datetime import date
import re

def Register_Customer():
    try:
        while True:
            print('------------------')
            Customer_Name = input('Customer Name:')
            if not Customer_Name or Customer_Name.strip() == "":
                print("SORRY! Customer name cannot be empty.")
            elif any(char.isdigit() for char in Customer_Name):
                print("SORRY! Customer name cannot contain numeric characters.")
            else:
                break
        
        
        
        while True:
            print('------------------')
            Customer_Phone = input('Customer Phone:')
            if not Customer_Phone or Customer_Phone.strip() == "":
                print("SORRY! Phone number cannot be empty.")
            elif not Customer_Phone.isdigit():
                print("SORRY! Phone number must contain only numeric characters.")
            elif len(Customer_Phone) != 10:
                print("SORRY! Phone number must be exactly 10 digits.")
            else:
                break
        
        
        
        while True:
            print('------------------')
            Customer_Email = input('Customer Email:')
            email_pattern = r"^[a-zA-Z0-9._%+-]+@(gmail|yahoo|[a-zA-Z0-9.-]+)\.com$"
            if not Customer_Email or Customer_Email.strip() == "":
                print("SORRY! Email cannot be empty.")
            elif not re.match(email_pattern, Customer_Email):
                print("SORRY! Invalid email format.")
            else:
                break
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

        while True:
            print('------------------')
            Product_Name = input('Product Name:')
            if not Product_Name or Product_Name.strip() == "":
                print("SORRY! Product name cannot be empty.")
            else:
                formatted_input = Product_Name.replace(" ", "").lower()
                cursor.execute('SELECT ProductName FROM Inventory')
                rows = cursor.fetchall()

                product_names = [row[0].replace(" ", "").lower() for row in rows]
                
                if formatted_input in product_names:
                    break
                else:
                    print("SORRY! Product name does not match any product in the inventory.")
        
        while True:
            print('------------------')
            Order_Quantity = input('Order Quantity:')
            if not Order_Quantity or Order_Quantity.strip() == "":
                print("SORRY! Order quantity cannot be empty.")
            elif not Order_Quantity.isdigit():
                print("SORRY! Order quantity must be a numeric value.")
            else:
                break
        
        while True:
            print('------------------')
            CustomerID = input('Customer ID:')
            if not CustomerID or CustomerID.strip() == "":
                print("SORRY! Customer ID cannot be empty.")
            elif not CustomerID.isdigit():
                print("SORRY! Customer ID must be numeric.")
            else:
                cursor.execute('SELECT CustomerID FROM customer WHERE CustomerID = ?', (CustomerID,))
                if cursor.fetchone():
                    break
                else:
                    print(f"SORRY! Customer ID {CustomerID} does not exist in the customer database.")
        while True:
            print('------------------')
            Shipping_Address = input('Shipping Address:')
            if not Shipping_Address or Shipping_Address.strip() == "":
                print("SORRY! Shipping address cannot be empty.")
            else:
                break
        
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
            cursor.execute('SELECT * FROM customer_orders where Status=? AND Shipped=?',('Open','No'))
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
            
            cursor.execute("SELECT OrderID FROM Assigned_Orders WHERE OrderID = ?", (OrderIs,))
            orderss = cursor.fetchone()
            if orderss:
                print('-------------------------------------------------------')
                print(f"Provided order ID {OrderIs} is already assigned to salesperson.")
                print('-------------------------------------------------------')
                continue

            cursor.execute('SELECT OrderID FROM customer_orders where Status=? AND Shipped=?',('Open','No'))
            Order_ID = [str(row[0]) for row in cursor.fetchall()]
            if Order_ID is not None and OrderIs in Order_ID:
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
    print('------------------------------------')
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

            cursor.execute("SELECT productStock FROM Inventory WHERE LOWER(REPLACE(ProductName,' ','')) = LOWER(REPLACE(?,' ',''))", (product_name,))
            stock = cursor.fetchone()

            if stock and stock[0] >= required_quantity:
                sufficient_inventory.append(order)
            else:
                insufficient_inventory.append(order)


        headers = ['Order ID', 'Order Date', 'Product Name', 'Quantity']

        print('Orders with Sufficient Stock:')
        print('-----------------------------')
        if sufficient_inventory:
            print(tabulate(pd.DataFrame(sufficient_inventory, columns=headers), headers='keys', tablefmt='grid', showindex=False))
        else:
            print('No orders with sufficient Stock.')

        print('   ')
        print('Orders with Insufficient Stock:')
        print('-------------------------------')
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
                Order_Id = int(input("Enter Order ID to schedule the job: "))
                cursor.execute("SELECT * FROM customer_orders WHERE OrderID = ? AND Status = 'Open'", (Order_Id,))
                order = cursor.fetchone()
                if not order:
                    print(f"No order found with ID {Order_Id}. Please enter a valid Order ID.")
                    continue
                cursor.execute("SELECT Quantity, ProductName FROM customer_orders WHERE OrderID = ? AND Status = 'Open'", (Order_Id,))
                order = cursor.fetchone()
                order_quantity=order[0]
                product_name=order[1]

                cursor.execute("SELECT productStock FROM Inventory WHERE LOWER(REPLACE(ProductName,' ','')) = LOWER(REPLACE(?,' ',''))", (product_name,))
                stock = cursor.fetchone()

                if stock and stock[0] < order_quantity:
                    print('----------------------------------')
                    print(f'Provided order {Order_Id} is Out of Stock.')
                    print(' ')
                    print('Unable to schedule the order.')
                    print('-----------------------------')
                    
                    continue
                
    
                cursor.execute("SELECT OrderID FROM Assigned_Orders WHERE OrderID = ?", (Order_Id,))
                orderss = cursor.fetchone()
                if not orderss:
                    print('-----------------------------------------------------------------------')
                    print(f"Provided order {Order_Id} is not yet assigned to salesperson by clerk.")
                    print(' ')
                    print('Please wait till order is assigned to sales person.')
                    print(' ')
                    print(f'Or contact to clerk regarding order {Order_Id} issue.')
                    print('-----------------------------------------------------------')
                    continue

                break
            except ValueError:
                print("Invalid input. Please enter a numeric Order ID.")

        
        while True:
            Start_Date = input("Enter Start Date (YYYY-MM-DD): ")
            End_Date = input("Enter End Date (YYYY-MM-DD): ")
            try:
                current_date = date.today()
                start_date = datetime.datetime.strptime(Start_Date, "%Y-%m-%d").date()
                end_date = datetime.datetime.strptime(End_Date, "%Y-%m-%d").date()
                if start_date > end_date:
                    print("Start date cannot be later than the end date. Please try again.")
                    print('---------------------------------------------------------------')
                    continue
                if start_date < current_date:
                    print('Start date cannot be in the past. Please try again.')
                    print('---------------------------------------------------')
                    continue
                break
            except ValueError:
                print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
                print('-------------------------------------------------------------')

        
        cursor.execute(
            """INSERT INTO Schedule_Jobs (OrderID, Job_Start_Date, Job_End_Date)
               VALUES (?, ?, ?)""",
            (Order_Id, Start_Date, End_Date,)
        )
        conn.commit()

        
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



def Order_Shipped():
        try:
            conn= sqlite3.connect('POPS.db')
            cursor = conn.cursor()
            cursor.execute(" SELECT OrderID, OrderDate, ProductName, Status, Shipped  FROM customer_orders WHERE Status= 'In Production' AND Shipped= 'No'")
            Records = cursor.fetchall()
            if Records:
                cursor.execute(" SELECT OrderID FROM customer_orders WHERE Shipped= 'No' AND Status= 'In Production'")
                RecordsIDs = cursor.fetchall()
                RecordsIDs = [str(record[0]) for record in RecordsIDs]
            else:
                print("No In Production orders available for Shipped.")
                return
            headers = ['Order ID', 'Order Date', 'Product Name',  'Status', 'Shipped']
            print(tabulate(Records, headers=headers, tablefmt="grid"))
            Order_ID=input('Enter order id to be shipped:')
            if Order_ID in RecordsIDs:
                cursor.execute("UPDATE customer_orders SET Shipped = 'Yes' WHERE OrderID = ?", (Order_ID,))
                conn.commit()
                print('-----------------------------------------')
                print(f" Order {Order_ID} is Successfully Shipped! ")
                print('-----------------------------------------')
            else:
                print('------------------')
                print('Id does not exists')
                print('------------------')

        except sqlite3.Error as e:
                print(f"An error occurred: {e}")
            
        finally:
                if conn:
                    conn.close()





def Order_Closed():
        try:
            conn= sqlite3.connect('POPS.db')
            cursor = conn.cursor()
            cursor.execute(" SELECT OrderID, OrderDate, ProductName, Status, Shipped  FROM customer_orders WHERE Shipped= 'Yes' AND Status= 'In Production'")
            Records = cursor.fetchall()
            if Records:
                cursor.execute(" SELECT OrderID FROM customer_orders WHERE Shipped= 'Yes' AND Status= 'In Production'")
                RecordsIDs = cursor.fetchall()
                RecordsIDs = [str(record[0]) for record in RecordsIDs]
            else:
                print("No Shipped orders available to close order.")
                return
            headers = ['Order ID', 'Order Date', 'Product Name',  'Status', 'Shipped']
            print(tabulate(Records, headers=headers, tablefmt="grid"))
            
            Order_ID=input('Enter order id to be shipped:')
            if Order_ID in RecordsIDs:
                
                cursor.execute("UPDATE customer_orders SET Status = 'Closed' WHERE OrderID = ?", (Order_ID,))
                conn.commit()
                print('-----------------------------------------')
                print(f" Order {Order_ID} is Successfully Closed! ")
                print('-----------------------------------------')
            else:
                print('------------------')
                print('Id does not exists')
                print('------------------')

        except sqlite3.Error as e:
                print(f"An error occurred: {e}")
            
        finally:
                if conn:
                    conn.close()




def Initiate_Billing():
        try:
            conn= sqlite3.connect('POPS.db')
            cursor = conn.cursor()
            cursor.execute(" SELECT OrderID, OrderDate, ProductName, Quantity, Status, Shipped  FROM customer_orders WHERE Shipped= 'Yes' AND Status= 'Closed'")
            Records = cursor.fetchall()
            if Records:
                cursor.execute(" SELECT OrderID FROM customer_orders WHERE Shipped= 'Yes' AND Status= 'Closed'")
                RecordsIDs = cursor.fetchall()
                RecordsIDs = [str(record[0]) for record in RecordsIDs]
            else:
                print("No Shipped orders available to close order.")
                return
            headers = ['Order ID', 'Order Date', 'Product Name', 'Quantity', 'Status', 'Shipped']
            print(tabulate(Records, headers=headers, tablefmt="grid"))
            
            Order_ID=input('Enter order id to initiate bill:')
            print('----------------------------------')
            if Order_ID in RecordsIDs:
                cursor.execute("SELECT ProductName FROM customer_orders WHERE OrderID=?",(Order_ID,))
                product_Name = cursor.fetchone()[0]
                cursor.execute("SELECT Quantity FROM customer_orders WHERE OrderID=?",(Order_ID,))
                Quantity = cursor.fetchone()[0]
                cursor.execute("SELECT Price_per_unit FROM Inventory WHERE LOWER(ProductName) = LOWER(?)", (product_Name,))
                price = cursor.fetchone()[0]
                item_total= Quantity*price
                print(f'{Quantity}x{product_Name}- ${price}={item_total}')
                tax= item_total *0.07
                grand_total= item_total+tax
                print(f'Subtotal: ${item_total:.2f}')
                print(f'Tax (7%): ${tax:.2f}')
                print('--------------------')
                print(f'Grand Total: ${grand_total:.2f}')            
                print('-----------------------------------------')
                print(f" Order {Order_ID} bill is successfully initiated! ")
                print('-----------------------------------------')
                print(f'Bill Amount is {grand_total:.2f}')
            else:
                print('------------------')
                print('Id does not exists')
                print('------------------')

        except sqlite3.Error as e:
                print(f"An error occurred: {e}")
            
        finally:
                if conn:
                    conn.close()



