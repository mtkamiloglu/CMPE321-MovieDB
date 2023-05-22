from flask import Flask, request, render_template, jsonify, session
import MySQLdb
import json
from .app import app, mysql_conn, cursor


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
