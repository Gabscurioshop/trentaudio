import psycopg2
from flask import Flask, flash
from config import config

def change_name(email, new_name):
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
        cur.execute("UPDATE USR SET USR_USERNAME = '" + new_name + "' WHERE USR_EMAIL = '" + email + "'")
        try:
            conn.commit()
        except psycopg2.Error as e:
            t_message = "Database error: " + e + "/n SQL: " + s
            print(t_message)
            return
            
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result
    return
