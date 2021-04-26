import psycopg2
from config import config

#creates search queries to retrieve audio file data
#returns audio_file_id, title and description of each file
def keyword(cur, query):
#keyword search
    cur.execute("CREATE VIEW KEYWORD_SEARCH AS SELECT * FROM KEYWORDS WHERE  '{}' ILIKE ANY(KEYWORD)" .format(query))
    cur.execute("SELECT AUDIO_FILE_ID, TITLE, DESCRIPTION FROM (KEYWORD_SEARCH NATURAL JOIN AUDIO_FILE)")
    rows = cur.fetchall()
    return rows
 
def interviewer(cur, query):
#interviewer search
    cur.execute("CREATE VIEW INTERVIEWER_SEARCH AS SELECT INTERVIEWER_ID FROM INTERVIEWER WHERE NAME ILIKE '{}%'".format(query))
    cur.execute("CREATE VIEW INTERVIEWER_AUDIO AS SELECT AUDIO_FILE_ID FROM (INTERVIEWER_SEARCH NATURAL JOIN INTERVIEWED_BY)")
    cur.execute("SELECT DISTINCT AUDIO_FILE_ID, TITLE, DESCRIPTION FROM (INTERVIEWER_AUDIO NATURAL JOIN AUDIO_FILE)")
    rows = cur.fetchall()
    return rows
    
def interviewee(cur, query):
#interviewee search
    cur.execute("CREATE VIEW INTERVIEWEE_SEARCH AS SELECT INTERVIEWEE_ID FROM INTERVIEWEE WHERE name ILIKE '{}%'".format(query))
    cur.execute("CREATE VIEW INTERVIEWEE_AUDIO AS SELECT AUDIO_FILE_ID FROM (INTERVIEWEE_SEARCH NATURAL JOIN INTERVIEW_OF)")
    cur.execute("SELECT DISTINCT AUDIO_FILE_ID, TITLE, DESCRIPTION FROM (INTERVIEWEE_AUDIO NATURAL JOIN AUDIO_FILE)")
    rows = cur.fetchall()
    return rows
    
def race(cur, query):
#race search
    cur.execute("CREATE VIEW RACE_SEARCH AS SELECT INTERVIEWEE_ID FROM INTERVIEWEE_RACES WHERE race ILIKE'{}%'".format(query)) 
    cur.execute("CREATE VIEW INTERVIEWEE_RACE_AUDIO AS SELECT AUDIO_FILE_ID FROM (RACE_SEARCH NATURAL JOIN INTERVIEW_OF)")
    cur.execute("SELECT DISTINCT AUDIO_FILE_ID, TITLE, DESCRIPTION FROM (INTERVIEWEE_RACE_AUDIO NATURAL JOIN AUDIO_FILE)")
    rows = cur.fetchall()
    return rows
     
def city(cur, query):
#city search
    cur.execute("CREATE VIEW CITY_SEARCH AS SELECT INTERVIEWEE_ID FROM INTERVIEWEE WHERE city ILIKE '{}%'".format(query))
    cur.execute("CREATE VIEW INTERVIEWEE_CITY_AUDIO AS SELECT AUDIO_FILE_ID FROM (CITY_SEARCH NATURAL JOIN INTERVIEW_OF)")
    cur.execute("SELECT DISTINCT AUDIO_FILE_ID, TITLE, DESCRIPTION FROM (INTERVIEWEE_CITY_AUDIO NATURAL JOIN AUDIO_FILE)")
    rows = cur.fetchall()
    return rows

def search_audio(choice, query):
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
        if (choice == 'Keywords'):
            rows = keyword(cur, query)
        elif (choice == 'Interviewer'):
            rows = interviewer(cur, query)
        elif (choice == 'Interviewee'):
            rows = interviewee(cur, query)
        elif (choice == 'Race'):
            rows = race(cur, query)
        elif (choice == 'City'):
            rows = city(cur, query)
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

