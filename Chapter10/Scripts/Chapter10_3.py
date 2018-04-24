# Chapter10_3.py
# Using pymapd and the mapd database to import geospatial data
# 20180215


import pymapd
from pymapd import connect
connection = connect(user="mapd", password= "Inter@ct1v!", 
	host="community.mapd.com", dbname="mapd")
import time
import shapefile
import pygeoif
cursor = connection.cursor()



insert = """INSERT INTO county
     VALUES ({count},'{name}','12','FL','{geom}');
"""
countyfile = r'data/FloridaCountiesSingle.shp'
# Read the County shapefile using the Reader class of the pyshp module
county_shapefile = shapefile.Reader(countyfile)
county_shapes = county_shapefile.shapes()
county_records = county_shapefile.records()

for count, record in enumerate(county_records[:100]):

    # Instantiate a county from the County class and populate the fields
    name = record[3]


    # Get the county geometry associated with the current record and convert it
    # into a pygeoif MultiPolygon, then into Well Known Text
    # for insertion into the data table
    county_geo = county_shapes[count]
    gshape = pygeoif.Polygon(pygeoif.geometry.as_shape(county_geo))
    geom = gshape.wkt
    print(geom[:40])
    insert_statement = insert.format(name=name, geom=geom,count=count+1)
    print('inserting')
    cursor.execute(insert_statement)
