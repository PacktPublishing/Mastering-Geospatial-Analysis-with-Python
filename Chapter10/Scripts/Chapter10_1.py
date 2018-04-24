# Chapter10_1.py
# Importing pymapd and testing the mapd GPU database
# 20180215


import pymapd
from pymapd import connect
connection = connect(user="mapd", password= "Inter@ct1v!", 
	host="community.mapd.com", dbname="mapd")
import time

cursor = connection.cursor()

print(time.time())
cursor.execute("SELECT * FROM city_of_carson_addresses")
print(cursor.rowcount)
print(time.time())
print(connection,cursor)
result = list(cursor)
print(result[:5])
print(time.time())

