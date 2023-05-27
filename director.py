from flask import Flask, request, render_template, jsonify, session
import MySQLdb
import json
from .app import app, mysql_conn, cursor


# directors should be able to list all theatres available for the given slot
@app.route('/director/list_theatres')
def list_theatres():
    return "<p>List Theatres</p>"


# directors should be able add movies
@app.route('/director/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'GET':
        return render_template('add_movie.html')
    else:
        movie_id = request.form.get('movie_id')
        movie_name = request.form.get('movie_name')
        duration = request.form.get('duration')
        director_user_name = session.get('username')
        genres = request.form.get('genre_list')

        query = "INSERT INTO Movie (movie_id, name, duration, average_rating, director_user_name, genres) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (movie_id, movie_name, duration, '0', director_user_name, genres))
        mysql_conn.commit()
        # movie sessiona ekleme
        return "<p>Movie is added</p>"


# directors should be able to add predeccessor to a movie
@app.route('/director/add_predecessor', methods=['GET', 'POST'])
def add_predecessor():
    if request.method == 'GET':
        return render_template('add_predecessor.html')
    else:
        movie_id = request.form.get('movie_id')
        predecessor_id = request.form.get('predecessor_movie_id')
        query = "INSERT INTO Predecessor (movie_id, predecessor_id) VALUES (%s, %s)"
        cursor.execute(query, (movie_id, predecessor_id))
        mysql_conn.commit()
        return "<p>Predecessor is added</p>"


# directors should be able to view all movies that they directed
@app.route('/director/view_movies', methods=['GET'])
def view_movies():
    director_user_name = session.get('username') 
    query ='''
        SELECT m.movie_id, m.name, ms.theatre_id, ms.time_slot, GROUP_CONCAT(p.predecessor_movie_id) AS predecessors
        FROM Movie AS m
        JOIN Movie_Session AS ms ON m.movie_id = ms.movie_id
        JOIN Predecessor AS p ON m.movie_id = p.movie_id
        WHERE m.director_user_name = %s
        GROUP BY m.movie_id, m.name, ms.theatre_id, ms.time_slot
    '''
    cursor.execute(query, [director_user_name])
    mysql_conn.commit()
    result = cursor.fetchall()
    jsonStr = json.dumps(result)
    jsonArr = json.loads(jsonStr)
    return render_template('view_movies.html', movies=jsonArr)


# directors should be able to view all audiences who bought a ticket for a movie directed by them
@app.route('/director/view_audiences', methods=['GET', 'POST'])
def view_audiences():
    if request.method == 'GET':
        return render_template('view_audiences.html')
    else:
        movie_id = request.form.get('movie_id')
        director_user_name = session.get('username')
        query = '''
            SELECT a.user_name, a.name, a.surname from Audience as a
            inner join Bought_Ticket as b on a.user_name = b.audience_user_name
            inner join Movie as m on b.movie_id = m.movie_id
            inner join Director as d on m.director_user_name = d.user_name
            where b.movie_id = %s and d.user_name = %s
            '''
        cursor.execute(query, (movie_id, director_user_name))
        mysql_conn.commit()
        result = cursor.fetchall()
        jsonStr = json.dumps(result)
        jsonArr = json.loads(jsonStr)
        return render_template('show_audiences.html', audiences=jsonArr)


# directors should be able to update the name of a movie directed by them
@app.route('/director/update_movie_name', methods=['GET', 'POST'])
def update_movie_name():
    if request.method == 'GET':
        return render_template('update_movie_name.html')
    else:
        movie_id = request.form.get('movie_id')
        new_movie_name = request.form.get('new_movie_name')

        query = "UPDATE Movie SET name = %s WHERE movie_id = %s"
        cursor.execute(query, (new_movie_name, movie_id))
        mysql_conn.commit()

        return "<p>Movie name updated successfully</p>"
