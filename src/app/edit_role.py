#changes user's role (by sadmin) in db- Coded by Carolyne
import psycopg2
from flask import Flask, flash
from config import config

def set_role(email, role):
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
        exists = cur.execute("SELECT * FROM CASUAL_USR WHERE USR_EMAIL = '" + email + "'")
        print(exists)
        if role == 'admin':
            cur.execute("UPDATE USR SET ROLE = 'admin' WHERE USR_EMAIL = '" + email + "'")
            if exists:
                cur.execute("DELETE FROM CASUAL_USR WHERE USR_EMAIL = '" + email + "'")
        elif role == 'user':
            cur.execute("UPDATE USR SET ROLE = 'user' WHERE USR_EMAIL = '" + email + "'")
            if not exists:
                cur.execute("INSERT INTO CASUAL_USR VALUES ('" + email + "', 'N')")
            
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
