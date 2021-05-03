import psycopg2
from flask import Flask, flash
from config import config
from werkzeug.security import generate_password_hash, check_password_hash

def verify_user(email, password):
    conn = None
    curr_user = None
    try:
        # read connection parameters from database.ini
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        cur.execute("SELECT USR_PASSWORD FROM USR WHERE USR_EMAIL = '{}'".format(email))
        curr_pass = cur.fetchone()[0]
   
        #print(curr_pass)
        #print(password)
        if check_password_hash(curr_pass, password):
            cur.execute("SELECT ROLE FROM USR WHERE USR_EMAIL = '{}'".format(email))
            curr_user = cur.fetchone()[0]
            print(curr_user)
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result
    if email == 'jefhirejfu84u44r4u8uru4':
        return 'logout'
    else:
        return curr_user
