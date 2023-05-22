from flask import Flask, request, render_template, jsonify, session
import MySQLdb
import json

app = Flask(__name__)
app.secret_key = 'super secret key'
 
HOST = 'localhost'
USER = 'root'
PASSWD = 'mydata'
DATABASE = 'moviesystem'

mysql_conn = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE)
cursor = mysql_conn.cursor()

from .audience import list_movies, buy_ticket, view_tickets
from .db_manager import login, add_user, delete_audience, update_platform_id, see_directors, see_ratings, see_movies, see_average_rating
from .director import director_login, list_theatres, add_movie, add_predecessor, view_movies, view_audiences, update_movie_name 


@app.route('/')
def hello():
    return render_template('manager_login.html')




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
@app.route('/manager/see_ratings')
def see_ratings():
    return "<p>See Ratings</p>"

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
        query = "INSERT INTO Predecessor (movie_id, predecessor_movie_id) VALUES (%s, %s)"
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

# audiences should be able to list all the movies
@app.route('/audience/list_movies')
def list_movies():
    return "<p>List Movies</p>"

# audiences sould be able to buy a movie ticket
@app.route('/audience/buy_ticket')
def buy_ticket():
    return "<p>Buy Ticket</p>"

# audiences should be able to view the tickets they bought
@app.route('/audience/view_tickets')
def view_tickets():
    return "<p>View Tickets</p>"