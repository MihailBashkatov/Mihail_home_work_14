# Импорт необходимых библиотек
import sqlite3
import json


def search_title(user_input):
    """ Поиск по названию"""

    with sqlite3.connect('netflix.db') as connection:
        result = connection.cursor()
        query = """SELECT title, country, release_year, listed_in, description
                             FROM netflix
                             WHERE title = ?
                             ORDER by release_year DESC
                             LIMIT 1
                        """
        result.execute(query, (user_input.title(),))
        movie = result.fetchall()
        chosen_movie = {}
        for item in movie:
            chosen_movie["title"] = item[0]
            chosen_movie["country"] = item[1]
            chosen_movie["release_year"] = item[2]
            chosen_movie["genre"] = item[3]
            chosen_movie["description"] = item[4].strip()
        return chosen_movie


def search_by_period(year_one, year_two):
    """ Поиск по диапазону лет выпуска."""

    with sqlite3.connect('netflix.db') as connection:
        result = connection.cursor()
        query = """SELECT title, release_year
                             FROM netflix
                             WHERE release_year BETWEEN ? and ?
                             ORDER by release_year DESC
                             LIMIT 30
                        """
        result.execute(query, (year_one, year_two))
        movies = result.fetchall()
        movies_by_period = []
        for movie in movies:
            chosen_movies = dict()
            chosen_movies["title"] = movie[0]
            chosen_movies["release_year"] = movie[1]
            movies_by_period.append(chosen_movies)
    return movies_by_period


def search_by_rating(user_rating):
    """ Поиск по  рейтингу"""

    with sqlite3.connect('netflix.db') as connection:
        result = connection.cursor()
        if user_rating.strip().lower() == "children".strip().lower():
            query = """SELECT title, rating, description
                           FROM netflix
                           WHERE rating = 'G'
                           LIMIT 100
                          """
            result.execute(query)
        elif user_rating.strip().lower() == "family".strip().lower():
            query = """SELECT title, rating, description
                            FROM netflix
                            WHERE rating = 'PG-13' OR  rating = 'G'
                            LIMIT 100
                          """
            result.execute(query)
        elif user_rating.strip().lower() == "adult".strip().lower():
            query = """SELECT title, rating, description
                             FROM netflix
                             WHERE rating = 'NC-17' OR  rating = 'R'
                             LIMIT 100
                          """
            result.execute(query)
        movies = result.fetchall()
        movies_by_rating = []
        for movie in movies:
            chosen_movies = dict()
            chosen_movies["title"] = movie[0]
            chosen_movies["rating"] = movie[1]
            chosen_movies["description"] = movie[2].strip()
            movies_by_rating.append(chosen_movies)
    return movies_by_rating


def search_new_by_genre(genre):
    """ Поиск по жанру"""

    with sqlite3.connect('netflix.db') as connection:
        result = connection.cursor()
        query = """SELECT title, description
                             FROM netflix
                             WHERE listed_in = ?
                             ORDER by release_year DESC
                             LIMIT 10
                        """
        result.execute(query, (genre,))
        movies = result.fetchall()
        chosen_movie_list = []
        for movie in movies:
            chosen_movie = dict()
            chosen_movie["title"] = movie[0]
            chosen_movie["description"] = movie[1].strip()
            chosen_movie_list.append(chosen_movie)
        return chosen_movie_list


def search_by_actors(actor_one, actor_two):
    """ Получает в качестве аргумента имена двух актеров,
           и возвращает список тех, кто играет с ними в паре больше 2 раз."""

    with sqlite3.connect('netflix.db') as connection:
        result = connection.cursor()
        query = """SELECT "cast"
                             FROM netflix
                             WHERE "cast" LIKE ?
                             AND "cast" LIKE ?
                        """
        result.execute(query, (('%' + actor_one + '%'), ('%' + actor_two + '%')))
        movies = result.fetchall()

        actors_str = ''
        for actor in movies:
            actor = ','.join(actor)
            actors_str += actor + ', '
        actors_list = actors_str.split(', ')
        actors_list_needed = []
        for act in actors_list:
            if actors_list.count(act) > 2 and act != actor_one and act != actor_two:
                if act in actors_list_needed:
                    continue
                actors_list_needed.append(act)
        return actors_list_needed


def search_by_types(type_chosen, year, genre):
    """ Получает в качестве аргумента  тип картины (фильм или сериал), год выпуска и ее жанр
          Возвращает список названий картин с их описаниями в JSON"""

    with sqlite3.connect('netflix.db') as connection:
        result = connection.cursor()
        query = """SELECT title, description
                             FROM netflix
                             WHERE type = ?
                              AND release_year = ?
                              AND listed_in = ?
                        """
        result.execute(query, (type_chosen, year, genre))
        movies = result.fetchall()
        movie_list = []
        for movie in movies:
            movie_dict = dict()
            movie_dict['title'] = movie[0]
            movie_dict["description"] = movie[1].strip()
            movie_list.append(movie_dict)
        return json.dumps(movie_list)
