import psycopg2
from config import config

def get_audio(aud_id):
#retrieve audio file data
    query = "SELECT * FROM AUDIO_FILE WHERE audio_file_id = '{}'" .format(aud_id)
    results = display(query)
    return results
    
def get_transcript(trans_id):
#retrieve transcript data
    query = "SELECT * FROM TRANSCRIPT WHERE audio_file_id = '{}'" .format(trans_id)
    results = display(query)
    return results
    
def display(query):
#Connect to database
    """ Connect to the PostgreSQL database server """
    conn = None
    row = ''
    try:
        # read connection parameters from database.ini
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the %s database from display...' % (params['database']))
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
