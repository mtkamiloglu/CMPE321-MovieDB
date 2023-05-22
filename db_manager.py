from flask import Flask, request, render_template, jsonify, session
import MySQLdb
import json
from .app import app, mysql_conn, cursor


# database managers should be able to login
@app.route('/manager/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        return render_template('manager_login.html')
    
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        query = "SELECT * FROM Database_Manager WHERE user_name = %s AND password = %s"
        cursor.execute(query, (username, password))
        mysql_conn.commit()
        result = cursor.fetchone()
        print(result)

        if result:
            return "<p>Login Successful</p>"
        else:
            return "<p>Username or password is wrong</p>"



# database managers should be able to add new users
@app.route('/manager/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('add_user.html')
    else:
        user_name = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        surname = request.form.get('surname')
        role = request.form.get('role')

        if role == 'director':
            nation = request.form.get('nation')
            platform_id = request.form.get('platform_id')
            query = "INSERT INTO Director (user_name, password, name, surname, nation, platform_id) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (user_name, password, name, surname, nation, platform_id))
            mysql_conn.commit()
            return "<p>Director is added</p>"
        
        else:
            query = "INSERT INTO Audience (user_name, password, name, surname) VALUES (%s, %s, %s, %s)"
            print(user_name, password, name, surname)
            cursor.execute(query, (user_name, password, name, surname))
            mysql_conn.commit()
            return "<p>Audience is added</p>"

# db managers should be able to delete audience
@app.route('/manager/delete_audience')
def delete_audience(): 
    return "<p>Delete Audience</p>"

# db managers should be able to update platform id
@app.route('/manager/update_platform_id')
def update_platform_id():
    return "<p>Update Platform ID</p>"

# db managers should be able to see all directors
@app.route('/manager/see_directors', methods=['GET', 'POST'])
def see_directors():
    query = "SELECT * FROM Director"
    cursor.execute(query)
    directors = cursor.fetchall()
    jsonStr = json.dumps(directors)
    jsonArr = json.loads(jsonStr)
    mysql_conn.commit()
    return render_template('see_directors.html', directors=jsonArr)

# db managers should be able to see all ratings of a user
@app.route('/manager/see_ratings')
def see_ratings():
    return "<p>See Ratings</p>"

# db managers should be able to see all movies of a director
@app.route('/manager/see_movies')
def see_movies():
    return "<p>See Movies</p>"

# db manager should be able to see average rating of a movie
@app.route('/manager/see_average_rating')
def see_average_rating():
    return "<p>See Average Rating</p>"