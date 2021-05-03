import psycopg2
from config import config
    
def md_query(cur, meta_desc, meta_type,af_id):#add md_edit requesr to database
    res = ''
    cur.execute("INSERT INTO REPORT (type, audio_file_id, usr_email, a_email, decision) VALUES ('md_edit','{}', 'vbradley@university.com', NULL, 'pending')".format(af_id))
    cur.execute("CREATE VIEW MAX_MD AS SELECT USR_EMAIL, MAX(REPORT_NUM) FROM REPORT WHERE TYPE='md_edit' GROUP BY USR_EMAIL")
    cur.execute("CREATE VIEW USR_MD AS SELECT MAX FROM MAX_MD WHERE USR_EMAIL = 'vbradley@university.com'")
    cur.execute("SELECT * FROM USR_MD")
    res = cur.fetchall()#fetch recent report 
    num = int(res[0][0])#get report id as integer
    cur.execute("INSERT INTO METADATA_EDIT_REQUEST VALUES ({},'{}','{}')".format(num,meta_desc,meta_type))
    #Drop views
    cur.execute("DROP VIEW USR_MD")
    cur.execute("DROP VIEW MAX_MD")
    print("Done executing.")
def edit_md(meta_desc,meta_type,af_id):
#Connect to database
    """ Connect to the PostgreSQL database server """
    conn = None
    row = ''
    try:
        # read connection parameters from database.ini
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the %s database from metadata...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
        conn.autocommit = True
        # create a cursor
        cur = conn.cursor()
        
        #add transcript error report to db
        md_query(cur, meta_desc,meta_type,af_id)
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

