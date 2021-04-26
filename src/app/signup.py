import psycopg2
from flask import Flask, flash
from config import config

def create_user(email, name, password):
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
        str1 = "INSERT INTO USR(USR_EMAIL, USR_USERNAME, USR_PASSWORD, ROLE) VALUES ("
        str1 += "'" + email + "',"
        str1 += " '" + name + "',"
        str1 += " '" + password + "',"
        str1 += " 'user')"
        cur.execute(str1)
        str2 = "INSERT INTO CASUAL_USR(USR_EMAIL, IS_BLOCKED) VALUES ("
        str2 += "'" + email + "',"
        str2 += " 'N')"
        cur.execute(str2)
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
    return
    
    
