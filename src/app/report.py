import psycopg2
from config import config

#def transcript_error(desc):
#add transcript error to database
    #query = "INSERT INTO REPORTS '{}'" .format(desc)
    #results = save_to_db(query)
    #return results
    
def save_to_db(query):
#Connect to database
    """ Connect to the PostgreSQL database server """
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
        cur.execute(query)
        row = cur.fetchall()
       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return row
