# pylint:disable=C0111,C0103

def order_rank_per_customer(db):
    query = """SELECT OrderID, CustomerID,  OrderDate,
            RANK() OVER (
            PARTITION BY CustomerID
            ORDER BY OrderDate)
            AS OrderRank
            FROM Orders"""

    db.execute(query)
    results = db.fetchall()
    return results

def order_cumulative_amount_per_customer(db):
    query = """
            WITH TempTable as (SELECT od.OrderDetailID, od.OrderID, ROUND(SUM(od.UnitPrice  * od.Quantity), 1) AS OrderTotal, o.OrderDate, o.CustomerID
            FROM OrderDetails od
            JOIN Orders o ON od.OrderID = o.OrderID
            GROUP BY od.OrderID
            ORDER BY o.CustomerID)

            SELECT OrderId, CustomerId, OrderDate,
            SUM(OrderTotal) OVER (
 	        PARTITION BY CustomerID
            ORDER BY OrderDate)
		    AS OrderCumulativeAmount
            FROM TempTable
            """

    db.execute(query)
    results = db.fetchall()
    return results
