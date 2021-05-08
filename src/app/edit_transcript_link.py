#change the link to the transcript for the file in db- Coded by Carolyne
import psycopg2
from config import config

def edit_t_link(r_num, new_link):
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
        cur.execute("UPDATE TRANSCRIPT SET FILE = '" + new_link + "' WHERE AUDIO_FILE_ID IN (SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "')")
        
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
    # return 
    return
