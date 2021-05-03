import psycopg2
from config import config

def privilege_display_users(query):
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
            cur.execute("SELECT USR_EMAIL, USR_USERNAME, ROLE FROM USR WHERE (USR_USERNAME ILIKE '{}' OR USR_EMAIL ILIKE '{}')".format(query, query))
            rows = cur.fetchall()
        else:
            cur.execute("SELECT USR_EMAIL, USR_USERNAME, ROLE FROM USR")
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
    
