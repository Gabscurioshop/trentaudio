#search all users by some query and show their blocked status along with their info (used by admins and super admins)- Coded by Carolyne
import psycopg2
from config import config

def display_users(query):
    conn = None
    rows = ''
    try:
        # read connection parameters from database.ini
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        if query:
            cur.execute("CREATE VIEW USR_MATCHES AS SELECT USR_EMAIL, USR_USERNAME FROM USR WHERE (USR_USERNAME ILIKE '{}' OR USR_EMAIL ILIKE '{}')".format(query, query))
            cur.execute("CREATE VIEW USR_INFO AS SELECT USR_EMAIL, USR_USERNAME, IS_BLOCKED FROM (USR_MATCHES NATURAL JOIN CASUAL_USR)")
            cur.execute("SELECT USR_EMAIL, USR_USERNAME, IS_BLOCKED FROM USR_INFO")
            rows = cur.fetchall()
        else:
            cur.execute("CREATE VIEW USR_INFO AS SELECT USR_EMAIL, USR_USERNAME, IS_BLOCKED FROM (USR NATURAL JOIN CASUAL_USR)")
            cur.execute("SELECT USR_EMAIL, USR_USERNAME, IS_BLOCKED FROM USR_INFO")
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
    
