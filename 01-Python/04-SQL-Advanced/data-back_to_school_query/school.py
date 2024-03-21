# pylint:disable=C0111,C0103

def students_from_city(db, city):
    """return a list of students from a specific city"""

    query = """
            SELECT *
            FROM students s
            WHERE birth_city = ?
            """
    params = (city,)
    db.execute(query, params)
    students = db.fetchall()

    return students
