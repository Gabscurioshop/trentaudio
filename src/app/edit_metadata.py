import psycopg2
from config import config

def edit_md(md_type, r_num, new_info):
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
        
        if md_type == 'Change ID':
            cur.execute("UPDATE AUDIO_FILE SET AUDIO_FILE_ID = '" + new_info + "' WHERE AUDIO_FILE_ID IN (SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "')")
        elif md_type == 'Change Date Uploaded':
            cur.execute("UPDATE AUDIO_FILE SET DATE_PUBLISHED = '" + new_info + "' WHERE AUDIO_FILE_ID IN (SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "')")
        elif md_type == 'Change Publisher':
            cur.execute("UPDATE AUDIO_FILE SET PUBLISHER = '" + new_info + "' WHERE AUDIO_FILE_ID IN (SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "')")
        elif md_type == 'Change Audio Language':
            cur.execute("UPDATE AUDIO_FILE SET A_LANGUAGE = '" + new_info + "' WHERE AUDIO_FILE_ID IN (SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "')")
        elif md_type == 'Change Date Interviewed':
            cur.execute("UPDATE AUDIO_FILE SET DATE_INTERVIEWED = '" + new_info + "' WHERE AUDIO_FILE_ID IN (SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "')")
        elif md_type == 'Change Title':
            cur.execute("UPDATE AUDIO_FILE SET TITLE = '" + new_info + "' WHERE AUDIO_FILE_ID IN (SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "')")
        elif md_type == 'Change Description':
            cur.execute("UPDATE AUDIO_FILE SET DESCRIPTION = '" + new_info + "' WHERE AUDIO_FILE_ID IN (SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "')")
        elif md_type == 'Change Transcriber':
            cur.execute("UPDATE TRANSCRIPT SET TRANSCRIBER = '" + new_info + "' WHERE AUDIO_FILE_ID IN (SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "')")
        elif md_type == 'Change Transcript Language':
            cur.execute("UPDATE TRANSCRIPT SET T_LANGUAGE = '" + new_info + "' WHERE AUDIO_FILE_ID IN (SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "')")
        elif md_type == 'Change Interviewer Gender':
            cur.execute("CREATE VIEW A_ID AS SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "'")
            cur.execute("CREATE VIEW INTERVIEW_A_ID AS SELECT INTERVIEWER_ID FROM INTERVIEWED_BY WHERE AUDIO_FILE_ID IN A_ID")
            cur.execute("UPDATE INTERVIEWER SET GENDER = '" + new_info + "' WHERE INTERVIEWER_ID IN INTERVIEW_A_ID")
        elif md_type == 'Change Interviewer Age':
            cur.execute("CREATE VIEW A_ID AS SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "'")
            cur.execute("CREATE VIEW INTERVIEW_A_ID AS SELECT INTERVIEWER_ID FROM INTERVIEWED_BY WHERE AUDIO_FILE_ID IN A_ID")
            cur.execute("UPDATE INTERVIEWER SET AGE = '" + new_info + "' WHERE INTERVIEWER_ID IN INTERVIEW_A_ID")
        elif md_type == 'Change Interviewer Name':
            cur.execute("CREATE VIEW A_ID AS SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "'")
            cur.execute("CREATE VIEW INTERVIEW_A_ID AS SELECT INTERVIEWER_ID FROM INTERVIEWED_BY WHERE AUDIO_FILE_ID IN A_ID")
            cur.execute("UPDATE INTERVIEWER SET NAME = '" + new_info + "' WHERE INTERVIEWER_ID IN INTERVIEW_A_ID")
        elif md_type == 'Change Interviewer Race':
            return
        elif md_type == 'Change Interviewee Gender':
            cur.execute("CREATE VIEW A_ID AS SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "'")
            cur.execute("CREATE VIEW INTERVIEW_A_ID AS SELECT INTERVIEWEE_ID FROM INTERVIEW_OF WHERE AUDIO_FILE_ID IN A_ID")
            cur.execute("UPDATE INTERVIEWEE SET GENDER = '" + new_info + "' WHERE INTERVIEWEE_ID IN INTERVIEW_A_ID")
        elif md_type == 'Change Interviewee Age':
            cur.execute("CREATE VIEW A_ID AS SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "'")
            cur.execute("CREATE VIEW INTERVIEW_A_ID AS SELECT INTERVIEWEE_ID FROM INTERVIEW_OF WHERE AUDIO_FILE_ID IN A_ID")
            cur.execute("UPDATE INTERVIEWEE SET AGE = '" + new_info + "' WHERE INTERVIEWEE_ID IN INTERVIEW_A_ID")
        elif md_type == 'Change Interviewee Name':
            cur.execute("CREATE VIEW A_ID AS SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "'")
            cur.execute("CREATE VIEW INTERVIEW_A_ID AS SELECT INTERVIEWEE_ID FROM INTERVIEW_OF WHERE AUDIO_FILE_ID IN A_ID")
            cur.execute("UPDATE INTERVIEWEE SET NAME = '" + new_info + "' WHERE INTERVIEWEE_ID IN INTERVIEW_A_ID")
        elif md_type == 'Change Interviewee Race':
            return
        elif md_type == 'Change Interviewee City':
            cur.execute("CREATE VIEW A_ID AS SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "'")
            cur.execute("CREATE VIEW INTERVIEW_A_ID AS SELECT INTERVIEWEE_ID FROM INTERVIEW_OF WHERE AUDIO_FILE_ID IN A_ID")
            cur.execute("UPDATE INTERVIEWEE SET CITY = '" + new_info + "' WHERE INTERVIEWEE_ID IN INTERVIEW_A_ID")
        elif md_type == 'Change Interviewee State':
            cur.execute("CREATE VIEW A_ID AS SELECT AUDIO_ID FROM REPORT WHERE REPORT_NUM = '" + r_num + "'")
            cur.execute("CREATE VIEW INTERVIEW_A_ID AS SELECT INTERVIEWEE_ID FROM INTERVIEW_OF WHERE AUDIO_FILE_ID IN A_ID")
            cur.execute("UPDATE INTERVIEWEE SET STATE = '" + new_info + "' WHERE INTERVIEWEE_ID IN INTERVIEW_A_ID")
            
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
