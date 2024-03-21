# pylint: disable=missing-docstring, C0103

def directors_count(db):
    """Return the number of directors contained in the database."""

    query = """SELECT COUNT(*)
            FROM directors"""
    db.execute(query)
    results = db.fetchone()[0]
    return results


def directors_list(db):
    """Return the list of all the directors sorted in alphabetical order."""

    query = """SELECT *
            FROM directors
            ORDER BY name ASC"""
    db.execute(query)
    results = db.fetchall()
    director_names = [item[0] for item in results]
    return director_names


def love_movies(db):
    """Returns the list of all movies which contain the exact word "love"
    in their title, sorted in alphabetical order."""

    query = """
    SELECT *
    FROM movies
    WHERE lower(title) LIKE "love"
    OR lower(title) LIKE "% love %"
    OR lower(title) LIKE "% love."
    OR lower(title) LIKE "% love,%"
    OR lower(title) LIKE "love,%"
    OR lower(title) LIKE "% love!%"
    OR lower(title) LIKE "% love?%"
    OR lower(title) LIKE "% love'%"
    OR lower(title) LIKE "love %"
    OR lower(title) LIKE "% love"

    ORDER BY title ASC
    """
    db.execute(query)
    results = db.fetchall()
    movie_titles = [item[0] for item in results]

    return movie_titles


def directors_named_like_count(db, name):
    """Return the number of directors which contain a given word in their name."""

    params = ("%" + name + "%",)

    query = '''SELECT COUNT(*)
            FROM directors
            WHERE LOWER(name) LIKE ?
            '''

    db.execute(query, params)
    results = db.fetchone()[0]

    return results


def movies_longer_than(db, min_length):
    """Return this list of all movies which are longer than a given duration,
    sorted in the alphabetical order."""

    params = (min_length,)
    query = """ SELECT *
            FROM movies
            WHERE minutes > ?
            ORDER BY title ASC
            """
    db.execute(query, params)

    results = db.fetchall()
    movie_titles = [item[0] for item in results]
    return movie_titles
