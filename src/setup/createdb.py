import psycopg2

#establishing the connection
conn = psycopg2.connect(user='lion', password='lion', host = 'localhost', port='5432')
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Preparing query to create a database
sql = '''CREATE database trentaudio''';

#Creating a database
cursor.execute(sql)
print("Database created successfully...")

#Closing the connection
conn.close()
