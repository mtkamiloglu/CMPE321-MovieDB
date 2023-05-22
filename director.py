from flask import Flask, request, render_template, jsonify, session
import MySQLdb
import json
from .app import app, mysql_conn, cursor


# directors should be able to login to the system
@app.route('/director/login', methods=['GET', 'POST'])
def director_login():
    if request.method == 'GET':
        return render_template('director_login.html')
    
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        query = "SELECT * FROM Director WHERE user_name = %s AND password = %s"
        cursor.execute(query, (username, password))
        mysql_conn.commit()
        result = cursor.fetchone()
        print(result)

        if result:
            session['username'] = username
            return "<p>Login Successful</p>"
        else:
            return "<p>Username or password is wrong</p>"


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


# direrectors should be able to view all movies that they directed
@app.route('/director/view_movies')
def view_movies():
    return "<p>View Movies</p>"

# directors should be able to view all audiences who bought a ticket for a movie directed by them
@app.route('/director/view_audiences')
def view_audiences():
    return "<p>View Audiences</p>"

# directors should be able to update the name of a movie directed by them
@app.route('/director/update_movie_name')
def update_movie_name():
    return "<p>Update Movie Name</p>"