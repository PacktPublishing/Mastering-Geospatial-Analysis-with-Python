import psycopg2
connection = psycopg2.connect(host='localhost', user='{user}',
	password='{password}', port="5432")
connection.autocommit = True
cursor = connection.cursor()
cursor.execute('CREATE DATABASE chapter122')
connection.close() 


connection = psycopg2.connect(dbname='chapter12', host='localhost',
 user='{user}', password='{password}', port="5432")
cursor = connection.cursor()
connection.autocommit = True
cursor.execute('CREATE EXTENSION postgis')
connection.close() 

