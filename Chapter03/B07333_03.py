import psycopg2
connection = psycopg2.connect(database="pythonspatial",user="postgres", password="postgres")
cursor = connection.cursor()
cursor.execute("CREATE TABLE art_pieces (id SERIAL PRIMARY KEY, code VARCHAR(255), location GEOMETRY)")
connection.commit()



import requests
url='http://coagisweb.cabq.gov/arcgis/rest/services/public/PublicAr t/MapServer/0/query'
params={"where":"1=1","outFields":"*","outSR":"4326","f":"json"}
r=requests.get(url,params=params)
data=r.json()
data["features"][0] 

for a in data["features"]:    
    code=a["attributes"]["ART_CODE"]    
    wkt="POINT("+str(a["geometry"]["x"])+" "+str(a["geometry"]["y"])+")"    
    if a["geometry"]["x"]=='NaN':        
        pass    
        else:        
            cursor.execute("INSERT INTO art_pieces (code, location) VALUES ({},ST_GeomFromText('{}'))".format(code, wkt)) connection.commit() 


from shapely.geometry import Point, MultiPoint
thepoints=[]
for a in data["features"]:    
    code=a["attributes"]["ART_CODE"]    
    p=Point(float(a["geometry"]["x"]),float(a["geometry"]["y"]))    
    thepoints.append(p)    
    if a["geometry"]["x"]=='NaN':        
        pass    
        else:        
            cursor.execute("INSERT INTO art_pieces (code, location) VALUES ('{}',ST_GeomFromText('{}'))".format(code, p.wkt)) connection.commit() 


cursor.execute("SELECT * from art_pieces") 
data=cursor.fetchall() 
data


from shapely.wkb import loads
aPoint=loads(data[0][2],hex=True) 
aPoint.wkt


cursor.execute("SELECT id,code,ST_AsBinary(location) from art_pieces") 
data=cursor.fetchall() 
data[0][2] 
from shapely.wkb import loads 
pNoHex=loads(bytes(data[0][2])) 
pNoHex.wkt

cursor.execute("SELECT code, ST_AsText(location) from art_pieces") 
data = cursor.fetchone()   


from shapely.wkt import loads 
pb=loads(data[1])
pb.coords[:] 


cursor.execute("SELECT UpdateGeometrySRID('art_pieces','location',4326)") 
cursor.execute("SELECT Find_SRID('public','art_pieces','location')") 
cursor.fetchall()


cursor.execute("SELECT code, ST_AsTexT(ST_Transform(location,3857)) from art_pieces") 
cursor.fetchone()


cursor.execute("SELECT ST_AsText(ST_Buffer(a.location,25.00,'quad_segs=2')) 
from pieces a WHERE a.code='101'")
cursor.fetchall()  


from shapely.geometry import Polygon 
from shapely.wkt import loads 
buff=loads(data[0][0]) 
buff


cursor.execute("SELECT ST_Distance(a.location::geography,b.location::geography) FROM art_pieces a, art_pieces b where a.name='101' AND b.name='102'") 
dist=cursor.fetchall() 
dist


cursor.execute("SELECT ST_Distance(a.location::geography,ST_GeometryFromText('POINT(-106.5 35.1)')::geography) FROM art_pieces a where a.name='101'")
cursor.fetchall()  


from shapely.geometry import Point 
p=Point(-106.5,35.1) 
cursor.execute("SELECT ST_Distance(a.location::geography,ST_GeometryFromText('{}')::geography) FROM art_pieces a where a.name='101'".format(p.wkt))
cursor.fetchall()


cursor.execute("SELECT code, ST_Distance(location::geography, ST_GeometryFromText('POINT(-106.591838300225 35.1555000000615)')::geography) as d from art_pieces LIMIT 5") 
cursor.fetchall()     


cursor.execute("SELECT code, ST_Distance(location::geography, ST_GeometryFromText('POINT(-106.591838300225 35.1555000000615)')::geography) as d from art_pieces ORDER BY location<->ST_GeometryFromText('POINT(-106.591838300225 35.1555000000615)') LIMIT 5") 
cursor.fetchall() 


from shapely.geometry import LineString 
from shapely.geometry import MultiLineString
connection = psycopg2.connect(database="pythonspatial",user="postgres",password="postgres")
cursor = c.cursor() 
cursor.execute("CREATE TABLE lines (id SERIAL PRIMARY KEY, location GEOMETRY)") 
thelines=[] 
thelines.append(LineString([(-106.635585,35.086972),(-106.621294,35 .124997)])) 
thelines.append(LineString([(-106.498309,35.140108),(-106.497010,35 .069488)])) 
thelines.append(LineString([(-106.663878,35.106459),(-106.586506,35 .103979)]))
mls=MultiLineString([((-106.635585,35.086972),(-106.621294,35.12499 7)),((-106.498309,35.140108),(-106.497010,35.069488)),((-106.663878 ,35.106459),(-106.586506,35.103979))])
for a in thelines:    
    cursor.execute("INSERT INTO lines (location) VALUES (ST_GeomFromText('{}'))".format(a.wkt)) 
    connection.commit() 


cursor.execute("SELECT id, ST_AsTexT(location) from lines") 
data=cursor.fetchall() 
data


cu.execute("SELECT id, ST_Length(location::geography) FROM lines ") 
cu.fetchall()


cu.execute("SELECT id, ST_Length(location::geography) FROM lines ORDER BY ST_Length(location::geography)") 
cu.fetchall()   


cu.execute("SELECT ST_Intersects(l.location::geography,ll.location::geometry) FROM lines l, lines ll WHERE l.id=1 AND ll.id=3") 
cu.fetchall()

cu.execute("SELECT ST_AsText(ST_Intersection(l.location::geography, ll.location::geometry)) FROM lines l, lines ll WHERE l.id=1 AND ll.id=3") 
cu.fetchall()


from shapely.geometry import Polygon
connection = psycopg2.connect(database="pythonspatial",user="postgres", password="postgres") 
cursor = conectionn.cursor() 
cursor.execute("CREATE TABLE poly (id SERIAL PRIMARY KEY, location GEOMETRY)") 
a=Polygon([(-106.936763,35.958191),(-106.944385,35.239293),(-106.452396,35.281908),(-106.407844,35.948708)]) 
cursor.execute("INSERT INTO poly (location) VALUES (ST_GeomFromText('{}'))".format(a.wkt)) 
connection.commit()


cur.execute("SELECT id, ST_Area(location::geography) from poly")
cur.fetchall()


isin=Point(-106.558743,35.318618) 
cur.execute("SELECT ST_Contains(polygon.location,ST_GeomFromText('{}')) FROM poly polygon WHERE polygon.id=1".format(isin.wkt)) 
cur.fetchall()


isin=Point(-106.558743,35.318618) 
cur.execute("SELECT ST_Intersects(ST_GeomFromText('{}')::geography,polygon.location::geometry) FROM poly polygon WHERE polygon.id=1".format(isin.wkt)) 
cur.fetchall() 


isin=LineString([(-106.55,35.31),(-106.40,35.94)]) 
cur.execute("SELECT ST_AsText(ST_Intersection(polygon.location,ST_GeomFromText('{}'))) FROM poly polygon WHERE polygon.id=1".format(isin.wkt)) 
cur.fetchall()




