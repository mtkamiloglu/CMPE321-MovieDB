# CMPE321-MovieDB

This is our third project for CMPE321 - Introduction to Database Systems. In this project, we utilized the database we created in our initial homework assignment. Our objective was to develop an application that enables users to interact with, observe, and manage the database effectively. To begin, you will encounter a login page where you can log in as a manager, director, or audience member. Once logged in, each user type will have access to different pages with specific functionalities catered to their role. Simply click on the page that interests you to explore its respective features.
## To Run App

First you should create a file and create a python environment there. For creating the python environment you should run:
````
python3 -m venv .venv
````
After creating environment you should activate this environment:
````
. .venv/bin/activate
````
Since you have created and activated the python environment you should install the Flask to your environment:
````
pip install Flask
````

Now we are ready to pull the project to locale. You should clone this repository by using this command:
````
git clone https://github.com/mtkamiloglu/CMPE321-MovieDB.git
````
Once you cloned our project to your directory you should create a file named _'.env'_ .  We will put our environment variables to this file and use them in our project. The content of this file should be like this:
````
HOST =                   # Location of your database. It can be 'localhost' or an IP address.
DB_USER =                # User name to connect to database
DB_PASSWD =              # Password to connect to database
DATABASE =               # Name of the database to be used
````
After these steps, now you are ready to run our application. To run our project:
````
flask run
````

Finally our project is up and running.

If you have encounter with a problem or have any other questions please reach out us from muhammet.kamiloglu@boun.edu.tr and huseyin.civi@boun.edu.tr emails.
