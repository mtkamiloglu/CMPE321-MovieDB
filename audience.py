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
    user_name = session.get('username')
    query = '''
        SELECT m.movie_id, m.name, ms.session_id, r.rate, m.average_rating
        FROM Audience as a
        JOIN Bought_Ticket AS bt ON a.user_name = bt.audience_user_name
        JOIN Movie AS m on bt.movie_id = m.movie_id
        JOIN Movie_Session AS ms ON bt.session_id = ms.session_id
        LEFT JOIN Rate AS r ON r.audience_user_name = bt.audience_user_name 
        AND r.movie_id = bt.movie_id
        WHERE bt.audience_user_name = %s
    '''
    cursor.execute(query, [user_name])
    result = cursor.fetchall()
    jsonStr = json.dumps(result)
    jsonArr = json.loads(jsonStr)
    mysql_conn.commit()
    return render_template('view_tickets.html', tickets=jsonArr)
