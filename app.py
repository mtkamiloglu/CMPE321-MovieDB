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
from .db_manager import add_user, delete_audience, update_platform_id, see_directors, see_ratings, see_movies, see_average_rating
from .director import list_theatres, add_movie, add_predecessor, view_movies, view_audiences, update_movie_name 


@app.route('/')
def hello():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if role == 'director':
            
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
            
        elif role == 'manager':

            query = "SELECT * FROM Database_Manager WHERE user_name = %s AND password = %s"
            cursor.execute(query, (username, password))
            mysql_conn.commit()
            result = cursor.fetchone()
            print(result)

            if result:
                return "<p>Login Successful</p>"
            else:
                return "<p>Username or password is wrong</p>"
            
        else:

            query = "SELECT * FROM Audience WHERE user_name = %s AND password = %s"
            cursor.execute(query, (username, password))
            mysql_conn.commit()
            result = cursor.fetchone()
            print(result)

            if result:
                return "<p>Login Successful</p>"
            else:
                return "<p>Username or password is wrong</p>"
            

