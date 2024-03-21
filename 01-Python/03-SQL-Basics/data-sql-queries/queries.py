# pylint: disable=C0103, missing-docstring
def detailed_movies(db):
    '''return the list of movies with their genres and director name'''

    query = """SELECT movies.title, movies.genres, directors.name
            FROM movies
            JOIN directors ON movies.director_id = directors.id
            """

    db.execute(query)
    results = db.fetchall()
    return list(results)


def late_released_movies(db):
    '''return the list of all movies released after their director death'''
    query = """SELECT movies.title
            FROM movies
            JOIN directors ON movies.director_id = directors.id
            WHERE directors.death_year < movies.start_year
            ORDER BY movies.title ASC"""

    db.execute(query)
    results = db.fetchall()
    movie_data = [item[0] for item in results]
    return movie_data


def stats_on(db, genre_name):
    '''return a dict of stats for a given genre'''
    query = """SELECT genres, count(*), AVG(minutes)
                FROM movies
                WHERE genres = ?
                GROUP BY genres"""

    params = (genre_name,)
    db.execute(query, params)
    results = db.fetchone()
    stats = {
    'genre': results[0],
    'number_of_movies': results[1],
    'avg_length': round(results[2], 2)
            }
    return stats


def top_five_directors_for(db, genre_name):
    '''return the top 5 of the directors with the most movies for a given genre'''

    query = """SELECT directors.name, count(*) as movie_count
            FROM movies
            JOIN directors ON movies.director_id = directors.id
            WHERE genres = ?
            GROUP BY directors.id
            ORDER BY movie_count DESC, directors.name ASC
            LIMIT 5"""

    params = (genre_name,)
    db.execute(query, params)
    results = db.fetchall()
    return results

def movie_duration_buckets(db):
    '''Return the movie counts grouped by bucket of 30 min duration.'''

    low_limit = 0
    high_limit = 30
    buckets_left = True
    buckets = []

    db.execute("SELECT MAX(minutes) FROM movies")
    max_minutes = db.fetchall()[0][0]

    while buckets_left:
        query = f"""SELECT MAX(minutes), count(*)
                FROM movies
                WHERE minutes >= {low_limit} AND minutes < {high_limit}"""

        db.execute(query)
        total_movies = db.fetchall()
        if total_movies[0][1]:
            buckets.append((high_limit, total_movies[0][1]))

        low_limit += 30
        high_limit += 30

        if low_limit > max_minutes:
            buckets_left = False
    return buckets

def top_five_youngest_newly_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''

    query = """SELECT directors.name, movies.start_year - directors.birth_year as debut_age
                FROM movies
                JOIN directors ON movies.director_id = directors.id
                WHERE debut_age NOTNULL
                GROUP BY directors.id
                ORDER BY debut_age ASC
                LIMIT 5"""

    db.execute(query)
    results = db.fetchall()
    return results
