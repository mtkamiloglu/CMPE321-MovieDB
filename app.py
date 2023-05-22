from flask import Flask, request, render_template, jsonify, session
import MySQLdb
import json

app = Flask(__name__)
app.secret_key = 'super secret key'
 
HOST = 'localhost'
USER = 'root'
PASSWD = 'tayyip2001'
DATABASE = 'movies'

mysql_conn = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE)
cursor = mysql_conn.cursor()

from .audience import list_movies, buy_ticket, view_tickets
from .db_manager import login, add_user, delete_audience, update_platform_id, see_directors, see_ratings, see_movies, see_average_rating
from .director import director_login, list_theatres, add_movie, add_predecessor, view_movies, view_audiences, update_movie_name 


@app.route('/')
def hello():
    return render_template('manager_login.html')

