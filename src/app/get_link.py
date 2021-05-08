#retrieves the transcript link of a specific audio file of a report in the db- Coded by Carolyne
import psycopg2
from config import config

def get_link(r_num):
    conn = None
    rows = ''
    t_link = None
    try:
        # read connection parameters from database.ini
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
        # create a cursor
        cur = conn.cursor()
        cur.execute("SELECT FILE FROM TRANSCRIPT WHERE AUDIO_FILE_ID IN (SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "')")
        t_link = cur.fetchone()[0]
        
         # close the communication with the PostgreSQL
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result
    return t_link
