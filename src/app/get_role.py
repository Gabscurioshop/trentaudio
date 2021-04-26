import psycopg2
from flask import Flask, flash
from config import config

def check_role(email):
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
        cur.execute("SELECT ROLE FROM USR WHERE USR_EMAIL = '{}'".format(email))
        curr_user = cur.fetchone()[0]
        
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result
    return curr_user
