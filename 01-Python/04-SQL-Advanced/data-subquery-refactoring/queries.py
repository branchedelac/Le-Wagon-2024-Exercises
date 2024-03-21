# pylint:disable=C0111,C0103


def get_average_purchase(db):
    """ return the average amount spent per order for each customer ordered by customer ID"""

    query = """
            WITH TempTable as (SELECT od.OrderDetailID, od.OrderID, SUM(od.UnitPrice  * od.Quantity) AS OrderTotal, o.CustomerID
            FROM OrderDetails od
            JOIN Orders o ON od.OrderID = o.OrderID
            GROUP BY od.OrderID
            ORDER BY o.CustomerID)

            SELECT CustomerId, ROUND(AVG(OrderTotal), 2) as OrderAverage
            FROM TempTable
            GROUP BY CustomerID
            ORDER BY CustomerID
            """

    db.execute(query)
    results = db.fetchall()
    return results


def get_general_avg_order(db):
    """Return the average amount spent per order"""
    query = """
            WITH TempTable
            AS (SELECT od.OrderDetailID, od.OrderID, SUM(od.UnitPrice  * od.Quantity)
            AS OrderTotal, o.CustomerID
            FROM OrderDetails od
            JOIN Orders o ON od.OrderID = o.OrderID
            GROUP BY od.OrderID
            ORDER BY o.CustomerID)

            SELECT ROUND(AVG(OrderTotal), 2)
            FROM TempTable"""

    db.execute(query)
    results = db.fetchone()[0]
    return results



def best_customers(db):
    """Return the customers who have an average purchase greater than the
    general average purchase."""

    query = """WITH TempTable AS (SELECT od.OrderDetailID, od.OrderID,
            o.CustomerID, SUM(od.UnitPrice  * od.Quantity) AS OrderTotal
            FROM OrderDetails od
            JOIN Orders o ON od.OrderID = o.OrderID
            GROUP BY od.OrderID
            ORDER BY o.CustomerID),

            CompTable AS (SELECT TempTable.CustomerID,
            AVG(TempTable.OrderTotal) AS OrderAvg,
            AVG(TempTable.OrderTotal) AS CustomerAvg
            FROM TempTable
            GROUP BY TempTable.CustomerID)

            SELECT CompTable.CustomerID, ROUND(CompTable.CustomerAvg, 2)
            FROM CompTable
            WHERE CompTable.CustomerAvg > ?
            ORDER BY CompTable.CustomerAvg DESC"""

    params = (get_general_avg_order(db),)
    db.execute(query, params)
    results = db.fetchall()
    return results


def top_ordered_product_per_customer(db):
    """return the list of the top ordered product by each customer
    based on the total ordered amount in USD"""

    query = """WITH TempTable as (SELECT od.ProductID, CustomerID, od.OrderID,
            SUM(od.UnitPrice  * od.Quantity) AS OrderTotal
            FROM OrderDetails od
            JOIN Orders o ON od.OrderID = o.OrderID
            GROUP BY o.CustomerID, od.ProductID)

            SELECT TempTable.CustomerID, TempTable.ProductID,
            ROUND(MAX(TempTable.OrderTotal),1)
            FROM TempTable
            GROUP BY TempTable.CustomerID
            ORDER BY TempTable.OrderTotal DESC"""

    db.execute(query)
    results = db.fetchall()
    return results


def average_number_of_days_between_orders(db):
    """return the average number of days between two consecutive orders of the same customer"""
    query = """SELECT *
            LAG(OrderDate) OVER(PARTITION BY Customers.CustomerID ORDER BY date) AS PreviousOrderDate
            FROM Orders
            JOIN Customers on CustomerID = Customers.CustomerID """

    db.execute(query)
    results = db.fetchall()
    return results
