import psycopg2
from flask import Flask, flash
from config import config

def check_status(email):
    conn = None
    status = None
    try:
        # read connection parameters from database.ini
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        cur.execute("SELECT IS_BLOCKED FROM CASUAL_USR WHERE USR_EMAIL = '{}'".format(email))
        status = cur.fetchone()[0]
        print(status)
        
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result
    return status
