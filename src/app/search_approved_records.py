#searches reports based on their type and if they are approved then display them in the date order entered (easrliest first vs. oldest first)- Coded by Carolyne
import psycopg2
from config import config

def display_approved_records(r_type, order):
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
        if r_type == 'Transcript Error':
            cur.execute("CREATE VIEW T_ERRORS AS SELECT REPORT_NUM, AUDIO_ID, USR_EMAIL, ERROR_DESCRIPTION, DATE_CREATED, DECISION FROM (REPORT NATURAL JOIN TRANSCRIPT_ERROR) WHERE DECISION = 'Approved'")
            if order == 'Recent First':
                cur.execute("SELECT * FROM T_ERRORS ORDER BY DATE_CREATED DESC")
                rows = cur.fetchall()
            elif order == 'Oldest First':
                cur.execute("SELECT * FROM T_ERRORS ORDER BY DATE_CREATED ASC")
                rows = cur.fetchall()
        elif r_type == 'Metadata Edit':
            cur.execute("CREATE VIEW MD_EDITS AS SELECT REPORT_NUM, AUDIO_ID, USR_EMAIL, EDIT_METADATA_DESCRIPTION, DATE_CREATED, DECISION FROM (REPORT NATURAL JOIN METADATA_EDIT_REQUEST) WHERE DECISION = 'Approved'")
            if order == 'Recent First':
                cur.execute("SELECT * FROM MD_EDITS ORDER BY DATE_CREATED DESC")
                rows = cur.fetchall()
            elif order == 'Oldest First':
                cur.execute("SELECT * FROM MD_EDITS ORDER BY DATE_CREATED ASC")
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
    
