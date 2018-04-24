# Chapter10_2.py
# Using pymapd and the mapd database to create a geospatial table
# 20180215


import pymapd
from pymapd import connect
connection = connect(user="mapd", password= "Inter@ct1v!", 
	host="community.mapd.com", dbname="mapd")
import time

cursor = connection.cursor()


DROP = "DROP TABLE COUNTY;"
create = """CREATE TABLE county ( id integer NOT NULL, 
	name VARCHAR(50), statefips VARCHAR(3), 
	stpostal VARCHAR(3), geom Polygon );
"""

print(time.time())
try:
	cursor.execute(DROP)
except:
	pass
cursor.execute(create)
connection.commit()
print(time.time())
