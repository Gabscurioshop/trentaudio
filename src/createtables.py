import psycopg2
#establishing the connection
conn = psycopg2.connect(database = 'trentaudio', user='lion', password='lion', host = 'localhost', port='5432')
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Create the tables by running create-tables.sql
for line in open ('create-tables.sql'):
    cursor.execute(line)
print("Tables created successfully...")

#Populate tables with data
for data in open('data.sql'):
    cursor.execute(data)
print("Data successfully added to tables...")

conn.close()
