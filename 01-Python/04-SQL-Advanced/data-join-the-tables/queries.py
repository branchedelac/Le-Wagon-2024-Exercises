# pylint:disable=C0111,C0103

def detailed_orders(db):
    '''return a list of all orders (order_id, customer.contact_name,
    employee.firstname) ordered by order_id'''

    query = """
            SELECT o.OrderID, c.ContactName, e.FirstName
            FROM Orders o
            JOIN Customers c ON o.CustomerID = c.CustomerID
            JOIN Employees e ON o.EmployeeID = e.EmployeeID
            """
    db.execute(query)
    results = db.fetchall()
    return results


def spent_per_customer(db):
    '''return the total amount spent per customer ordered by ascending total
    amount (to 2 decimal places)
    Exemple :
        Jean   |   100
        Marc   |   110
        Simon  |   432
        ...
    '''

    query = """
            SELECT c.ContactName,
            ROUND(SUM(UnitPrice * Quantity), 2) as TotalSpend
            FROM Orders o
            JOIN Customers c ON o.CustomerID = c.CustomerID
            JOIN OrderDetails od ON o.OrderID  = od.OrderID
            GROUP BY c.CustomerID
            ORDER BY TotalSpend ASC
            """

    db.execute(query)
    results = db.fetchall()
    return results


def best_employee(db):
    '''Implement the best_employee method to determine who’s the best employee!
    By “best employee”, we mean the one who sells the most.
    We expect the function to return a tuple like: ('FirstName', 'LastName',
    6000 (the sum of all purchase)).
    The order of the information is irrelevant'''

    query = """
            SELECT e.FirstName, e.LastName,
            ROUND(SUM(UnitPrice * Quantity), 2) as TotalSold
            FROM Orders o
            JOIN Employees e ON o.EmployeeID = e.EmployeeID
            JOIN OrderDetails od ON o.OrderID  = od.OrderID
            GROUP BY e.EmployeeID
            ORDER BY TotalSold DESC
            """

    db.execute(query)
    results = db.fetchone()
    return results

def orders_per_customer(db):
    '''Return a list of tuples where each tuple contains the contactName
    of the customer and the number of orders they made (contactName,
    number_of_orders). Order the list by ascending number of orders'''

    query = """
            SELECT c.ContactName, COUNT(o.OrderID) as TotalOrders
            FROM Customers c
            LEFT JOIN Orders o ON o.CustomerID = c.CustomerID
            GROUP BY c.CustomerID
            ORDER BY TotalOrders ASC
            """
    db.execute(query)
    results = db.fetchall()
    return results
