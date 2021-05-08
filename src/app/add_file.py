#adds file to database- Coded by Carolyne
import psycopg2
from flask import Flask, flash
from config import config

def create_file(a_id, title, d_pub, pub, desc, a_lang, a_file, d_interview, interviewer, interviewee, t_file, transcriber, t_lang):
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
        str1 = "INSERT INTO AUDIO_FILE(AUDIO_FILE_ID, DATE_PUBLISHED, PUBLISHER, A_LANGUAGE, DATE_INTERVIEWED, TITLE, DESCRIPTION, FILE) VALUES ("
        str1 += "'" + a_id + "',"
        str1 += " '" + d_pub + "',"
        str1 += " '" + pub + "',"
        str1 += " '" + a_lang + "',"
        str1 += " '" + d_interview + "',"
        str1 += " '" + title + "',"
        str1 += " '" + desc + "',"
        str1 += " '" + a_file + "')"
        cur.execute(str1)
        
        str2 = "INSERT INTO TRANSCRIPT(AUDIO_FILE_ID, TRANSCRIBER, T_LANGUAGE, FILE) VALUES ("
        str2 += "'" + a_id + "',"
        str2 += " '" + transcriber + "',"
        str2 += " '" + t_lang + "',"
        str2 += " '" + t_file + "')"
        cur.execute(str2)
        
        cur.execute("SELECT INTERVIEWER_ID FROM INTERVIEWER WHERE INTERVIEWER_ID = '{}'".format(interviewer))
        curr_inter = cur.fetchone()[0]
        if not curr_inter:
            cur.execute("INSERT INTO INTERVIEWER(INTERVIEWER_ID, GENDER, AGE, NAME) VALUES ('" + interviewer + "', NULL, NULL, NULL)")
        
        str3 = "INSERT INTO INTERVIEWED_BY(AUDIO_FILE_ID, INTERVIEWER_ID) VALUES ("
        str3 += "'" + a_id + "',"
        str3 += " '" + interviewer + "')"
        cur.execute(str3)
        
        cur.execute("SELECT INTERVIEWEE_ID FROM INTERVIEWEE WHERE INTERVIEWEE_ID = '{}'".format(interviewee))
        curr_intee = cur.fetchone()[0]
        if not curr_intee:
            cur.execute("INSERT INTO INTERVIEWEE(INTERVIEWEE_ID, GENDER, AGE, NAME, CITY, STATE) VALUES ('" + interviewer + "', NULL, NULL, NULL, NULL, NULL)")
            
        str4 = "INSERT INTO INTERVIEW_OF(AUDIO_FILE_ID, INTERVIEWEE_ID) VALUES ("
        str4 += "'" + a_id + "',"
        str4 += " '" + interviewee + "')"
        cur.execute(str4)
        
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
    
    
