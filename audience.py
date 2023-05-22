from flask import Flask, request, render_template, jsonify, session
import MySQLdb
import json
from .app import app, mysql_conn, cursor


# audiences should be able to list all the movies
@app.route('/audience/list_movies', methods=['GET'])
def list_movies():
    query1 = '''
    SELECT m.movie_id, m.name, d.surname, d.platform_id, ms.theatre_id, ms.time_slot FROM Movie as m
    join Director as d on d.user_name = m.director_user_name
    join Movie_Session as ms on ms.movie_id = m.movie_id
    '''
    cursor.execute(query1)
    movies = cursor.fetchall()
    jsonStr = json.dumps(movies)
    movieInfos = json.loads(jsonStr)
    query2 = '''
    SELECT predecessor_movie_id FROM movies.Predecessor
    where movie_id=20005;
    '''
    cursor.execute(query2)
    predecessorsList = cursor.fetchall()
    print(predecessorsList)
    mysql_conn.commit()
    return render_template('list_movies.html', movies=movieInfos)

    

# audiences sould be able to buy a movie ticket
@app.route('/audience/buy_ticket')
def buy_ticket():
    return "<p>Buy Ticket</p>"

# audiences should be able to view the tickets they bought
@app.route('/audience/view_tickets')
def view_tickets():
    return "<p>View Tickets</p>"
