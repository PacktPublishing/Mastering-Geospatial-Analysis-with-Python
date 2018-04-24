# Chapter10_4.py
# Contains statements with pymapd and the mapd GPU database
# 20180215


import pymapd
from pymapd import connect
connection = connect(user="mapd", password= "Inter@ct1v!", 
	host="community.mapd.com", dbname="mapd")
import time

point = "POINT(-80.896146 27.438610)"
cursor = connection.cursor()
print(time.time())
sql_statement = "SELECT name FROM county where ST_Contains(geom,'{0}');".format(point)
#sql_statement = "SELECT name,ST_Contains(geom,'{0}') FROM county ;".format(point)

cursor.execute(sql_statement)

print(time.time())
results = list(cursor)
for result in results:
	print(result)
print(time.time())
