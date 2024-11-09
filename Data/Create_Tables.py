import sqlite3 

def creating_tables(file_name):
    folder_name = '.'
    customer_table = """
            CREATE TABLE if not exists customer (
            CustomerID INTEGER PRIMARY KEY,
            CustomerName TEXT,
            CustomerPhone INTEGER)
            """
    customer_orders_table = """
            CREATE TABLE if not exists customer_orders (
            OrderID INTEGER PRIMARY KEY,
            ProductName TEXT,
            Quantity INTEGER,
            ProductID INTEGER,
            CustomerID INTEGER,
            SalespersonID INTEGER,
            Status TEXT,
            Shipped TEXT,
            Remarks TEXT,
            FOREIGN KEY (ProductID) REFERENCES Inventory(ProductID),
            FOREIGN KEY (CustomerID) REFERENCES customer(CustomerID),
            FOREIGN KEY (SalespersonID) REFERENCES SalesPersons(SalesPersonID))
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

    ProductionTeam_table="""
    CREATE TABLE if not exists ProductionTeam (
    ProductionTeamID INTEGER PRIMARY KEY,
    ProductionTeamName TEXT)
    """

    AssignedOrders_table="""
    CREATE TABLE if not exists AssignedOrders (
    ProductionTeamID INTEGER,
            OrderID INTEGER,
            FOREIGN KEY (ProductionTeamID) REFERENCES ProductionTeam(ProductionTeamID),
            FOREIGN KEY (OrderID) REFERENCES orders(OrderID))
    """


    connection = sqlite3.connect(folder_name +'/' + file_name)

    try:
        cursor = connection.cursor()
        cursor.execute(customer_table)
        cursor.execute(customer_orders_table)
        cursor.execute(Inventory_table)
        cursor.execute(SalesPerson_table)
        cursor.execute(ProductionTeam_table)
        cursor.execute(AssignedOrders_table)
        connection.commit()
        print('Inside try')
    except sqlite3.Error as e:
        print(e)
    else:
        print(f'created all tables in {file_name}')
