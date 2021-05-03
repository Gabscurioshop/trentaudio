import psycopg2
from config import config
    
def trans_report(cur, err_desc,af_id):
    res = ''
    cur.execute("INSERT INTO REPORT (type,audio_id, usr_email, a_email, decision, date_created) VALUES ('trans_error','{}', 'vbradley@university.com', NULL,'pending',current_timestamp)".format(af_id))
    cur.execute("CREATE VIEW MAX_TRANS AS SELECT USR_EMAIL, MAX(REPORT_NUM) FROM REPORT WHERE TYPE='trans_error' GROUP BY USR_EMAIL")
    cur.execute("CREATE VIEW USR_ERR AS SELECT MAX FROM MAX_TRANS WHERE USR_EMAIL = 'vbradley@university.com'")
    cur.execute("SELECT * FROM USR_ERR")
    res = cur.fetchall()#fetch recent report 
    num = int(res[0][0])#get report id as integer
 
    cur.execute("INSERT INTO TRANSCRIPT_ERROR VALUES ({},'{}')".format(num,err_desc))
    #Drop views
    cur.execute("DROP VIEW USR_ERR")
    cur.execute("DROP VIEW MAX_TRANS")
    print("Done executing.")
def add_error(err_desc, af_id):
#Connect to database
    """ Connect to the PostgreSQL database server """
    conn = None
    row = ''
    try:
        # read connection parameters from database.ini
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the %s database from report...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
        conn.autocommit = True
        # create a cursor
        cur = conn.cursor()
        
        #add transcript error report to db
        trans_report(cur, err_desc,af_id)
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
