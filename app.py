from flask import Flask, request, render_template
import MySQLdb

app = Flask(__name__)
 
HOST = 'localhost'
USER = 'root'
PASSWD = 'tayyip2001'
DATABASE = 'sys'

mysql_conn = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE)
cursor = mysql_conn.cursor()

@app.route('/')
def hello():
    return "<p>Hello, World!</p>"

# database managers should be able to login
@app.route('/manager/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        return render_template('login.html')
    
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        query = "SELECT * FROM Database_Manager WHERE user_name = %s AND password = %s"
        cursor.execute(query, (username, password))

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
@app.route('/manager/see_directors')
def see_directors():
    return "<p>See Directors</p>"

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

# directors should be able to login to the system
@app.route('/director_login')
def director_login():
    return "<p>Director Login</p>"

# directors should be able to list all theatres available for the given slot
@app.route('/director/list_theatres')
def list_theatres():
    return "<p>List Theatres</p>"

# directors should be able add movies
@app.route('/director/add_movie')
def add_movie():
    return "<p>Add Movie</p>"

# directors should be able to add predeccessor to a movie
@app.route('/director/add_predecessor')
def add_predecessor():
    return "<p>Add Predecessor</p>"

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