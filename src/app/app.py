#! /usr/bin/python3

"""
ONE-TIME SETUP

To run this example in the CSC 315 VM you first need to make
the following one-time configuration changes:

# set the postgreSQL password for user 'lion'
sudo -u postgres psql
    ALTER USER lion PASSWORD 'lion';
    \q

# install pip for Python 3
sudo apt update
sudo apt install python3-pip

# install psycopg2
pip3 install psycopg2-binary

# install flask
pip3 install flask

# logout, then login again to inherit new shell environment
"""

"""
CSC 315
Spring 2021
John DeGood

# usage
export FLASK_APP=app.py 
flask run

# then browse to http://127.0.0.1:5000/

Purpose:
Demonstrate Flask/Python to PostgreSQL using the psycopg adapter.
Connects to the 7dbs database from "Seven Databases in Seven Days"
in the CSC 315 VM.

For psycopg documentation:
https://www.psycopg.org/

This example code is derived from:
https://www.postgresqltutorial.com/postgresql-python/
https://scoutapm.com/blog/python-flask-tutorial-getting-started-with-flask
https://www.geeksforgeeks.org/python-using-for-loop-in-flask/
"""

import psycopg2
from config import config
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
 
def connect(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters from database.ini
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall()
        cur.execute(query)
        rows = cur.fetchall()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows
 
# app.py

#create application object
app = Flask(__name__)

app.secret_key = "My precious"

#login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap
  
#use decorators to link functino to url
@app.route("/")
@login_required
def home():
    #return "Welcome to Trentaudio!" #return string
    return render_template('index.html') #render template
@app.route('/welcome')
def welcome():
    return render_template('welcome.html') #render template
 
#handle login requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] =True
            flash('You were just logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))

#def form():
 #   return render_template('my-form.html')

# handle form data
#@app.route('/form-handler', methods=['POST'])
#def handle_data():
 #   rows = connect(request.form['query'])

   # return render_template('my-result.html', rows=rows)

if __name__ == '__main__':
    app.run(debug = True)
