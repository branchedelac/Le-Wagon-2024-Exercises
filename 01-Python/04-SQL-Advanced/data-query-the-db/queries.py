# pylint:disable=C0111,C0103

def query_orders(db):
    """Returns a list of orders displaying each column."""

    query = """
    SELECT *
    FROM Orders
    """
    db.execute(query)
    results = db.fetchall()

    return results

def get_orders_range(db, date_from, date_to):
    """Returns a list of orders displaying all columns with OrderDate between
    date_from and date_to (excluding date_from and including date_to)."""

    query = """
    SELECT *
    FROM Orders
    WHERE OrderDate > ? AND OrderDate < ?
    LIMIT 5
    """

    params = (date_from, date_to,)

    db.execute(query, params)
    results = db.fetchall()

    return results


def get_waiting_time(db):
    """Gets a list with all the orders displaying each column and
    calculate an extra TimeDelta column displaying the number of days
    between OrderDate and ShippedDate, ordered by ascending TimeDelta"""

    query = """
            SELECT *, julianday(ShippedDate) - julianday(OrderDate) as TimeDelta
            FROM Orders
            ORDER BY TimeDelta ASC

            """

    db.execute(query)
    results = db.fetchall()
    return results
