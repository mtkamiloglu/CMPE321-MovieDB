from flask import Flask, request, render_template, jsonify, session
import MySQLdb
import json
from .app import app, mysql_conn, cursor


# database managers should be able to login
# @app.route('/manager/login', methods=['GET', 'POST'])
# def login():
    
#     if request.method == 'GET':
#         return render_template('manager_login.html')
    
#     else:
#         username = request.form.get('username')
#         password = request.form.get('password')

#         query = "SELECT * FROM Database_Manager WHERE user_name = %s AND password = %s"
#         cursor.execute(query, (username, password))
#         mysql_conn.commit()
#         result = cursor.fetchone()
#         print(result)

#         if result:
#             return "<p>Login Successful</p>"
#         else:
#             return "<p>Username or password is wrong</p>"



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
@app.route('/manager/delete_audience', methods=['GET', 'POST'])
def delete_audience():
    if request.method == 'GET':
        return render_template('delete_user.html')
    
    else:
        username = request.form.get('username')
        
        query = "DELETE FROM Audience WHERE user_name = %s"
        cursor.execute(query, [username])
        
        is_empty = False
        if cursor.rowcount == 0:
            is_empty = True
        
        bought_ticket_query = " DELETE FROM bought_ticket WHERE audience_user_name = %s"
        cursor.execute(bought_ticket_query, [username])
        
        subscription_query = "DELETE FROM Subscription WHERE audience_user_name = %s"
        cursor.execute(subscription_query, [username]) 
        
        mysql_conn.commit()
                
        if is_empty:
            return "<p>User not found</p>"
        else:
            return "<p>User deleted successfully</p>"



# db managers should be able to update platform id
@app.route('/manager/update_platform_id', methods=['GET','POST'])
def update_platform_id():
    if request.method == 'GET':
        return render_template('update_platform_id.html')
    else:
        director_user_name = request.form.get('director_username')
        platform_id = request.form.get('platform_id')
        query = "UPDATE Director SET platform_id = %s WHERE user_name = %s"
        cursor.execute(query, (platform_id, director_user_name))
        mysql_conn.commit()
        return "<p>Platform id is updated</p>"


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
@app.route('/manager/see_ratings', methods=['GET', 'POST'])
def see_ratings():
    if request.method == 'GET':
        return render_template('see_ratings.html')
    
    else:
        username = request.form.get('username')
        
        query = """
        SELECT M.movie_id, M.name, R.rate
        FROM Rate R
        INNER JOIN Movie M ON R.movie_id = M.movie_id
        WHERE R.audience_user_name = %s
        """
        cursor.execute(query, [username])
        result = cursor.fetchall()
        
        return render_template('ratings_list.html', ratings=result)



# db managers should be able to see all movies of a director
@app.route('/manager/see_movies', methods=['GET', 'POST'])
def see_movies():
    if request.method == 'GET':
        return render_template('see_movies.html')
    else:
        director_user_name = request.form.get('username')
        query = '''SELECT m.movie_id, m.name, ms.theatre_id, t.district, ms.time_slot
                FROM Movie_Session ms
                JOIN Movie m ON ms.movie_id = m.movie_id
                JOIN Theatre t ON ms.theatre_id = t.theatre_id
                WHERE m.director_user_name = %s'''

        cursor.execute(query, [director_user_name])
        movies = cursor.fetchall()
        jsonStr = json.dumps(movies)
        jsonArr = json.loads(jsonStr)
        mysql_conn.commit()
        return render_template('show_movies.html', movies=jsonArr)

# db manager should be able to see average rating of a movie
@app.route('/manager/see_average_rating', methods=['GET', 'POST'])
def see_average_rating():
    if request.method == 'GET':
        return render_template('see_average_rating.html')
    else:
        movie_id = request.form.get('movie_id')
        query = "SELECT movie_id, name, average_rating FROM Movie WHERE movie_id = %s"
        cursor.execute(query, [movie_id])
        result = cursor.fetchone()
        mysql_conn.commit()
        return render_template('show_average_rating.html', result=result)