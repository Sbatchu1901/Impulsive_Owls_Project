import sqlite3 

def creating_tables(file_name):
    folder_name = '.'
    customer_table = """
            CREATE TABLE if not exists customer (
            CustomerID INTEGER PRIMARY KEY,
            CustomerName TEXT,
            CustomerPhone INTEGER, CustomerEmail TEXT)
            """
    customer_orders_table = """
            CREATE TABLE if not exists customer_orders (
            OrderID INTEGER PRIMARY KEY,
            ProductName TEXT,
            Quantity INTEGER,
            CustomerID INTEGER,
            ShippingAddress TEXT,
            Status TEXT,
            Shipped TEXT,
            Remarks TEXT,
            FOREIGN KEY (CustomerID) REFERENCES customer(CustomerID))
            """
    Inventory_table="""
    CREATE TABLE if not exists Inventory (
    ProductID INTEGER PRIMARY KEY,
    ProductName TEXT,
    productStock INTEGER)
    """

    SalesPerson_table="""
    CREATE TABLE if not exists SalesPersons (
    SalesPersonID INTEGER PRIMARY KEY,
    SalesPersonName TEXT,
    SalesPersonContact INTEGER,
    SalesPersonEmail TEXT)
    """

    Schedule_Jobs = """
    CREATE TABLE Schedule_Jobs (
    ScheduleJobID INTEGER PRIMARY KEY,
    OrderID INTEGER,
    Job_Start_Date TEXT,
    Job_End_Date TEXT,
    FOREIGN KEY (OrderID) REFERENCES customer_orders(OrderID));
    """

    Assigned_Orders="""CREATE TABLE Assigned_Orders (
    AssignedID INTEGER PRIMARY KEY,
    OrderID INTEGER,
    SalesPersonID INTEGER,
    FOREIGN KEY (OrderID) REFERENCES Customer_Orders(OrderID),
    FOREIGN KEY (SalesPersonID) REFERENCES SalesPersons(SalesPersonID)
);"""


    connection = sqlite3.connect(folder_name +'/' + file_name)

    try:
        cursor = connection.cursor()
        cursor.execute(customer_table)
        cursor.execute(customer_orders_table)
        cursor.execute(Inventory_table)
        cursor.execute(SalesPerson_table)
        cursor.execute(Schedule_Jobs)
        cursor.execute(Assigned_Orders)
        connection.commit()
        print('Inside try')
    except sqlite3.Error as e:
        print(e)
    else:
        print(f'created all tables in {file_name}')
