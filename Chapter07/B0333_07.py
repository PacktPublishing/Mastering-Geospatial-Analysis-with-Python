import psycopg2 
import requests 
from shapely.geometry import Point,Polygon,MultiPolygon, mapping 
import datetime

connection = psycopg2.connect(database="pythonspatial",user="postgres", password="postgres") 
cursor = connection.cursor()
cursor.execute("CREATE TABLE areacommand (id SERIAL PRIMARY KEY, name VARCHAR(20), geom GEOMETRY)")
cursor.execute("CREATE TABLE beats (id SERIAL PRIMARY KEY, beat VARCHAR(6), agency VARCHAR(3), areacomm VARCHAR(15),geom GEOMETRY)")
cursor.execute("CREATE TABLE incidents (id SERIAL PRIMARY KEY, address VARCHAR(72), crimetype VARCHAR(255), date DATE,geom GEOMETRY)")
connection.commit() 


url='http://coagisweb.cabq.gov/arcgis/rest/services/public/adminboundaries/MapServer/8/query' 
params={"where":"1=1","outFields":"*","outSR":"4326","f":"json"} 
r=requests.get(url,params=params) 
data=r.json()
for acmd in data['features']:    
    polys=[]
    for ring in acmd['geometry']['rings']:        
        polys.append(Polygon(ring))    
    p=MultiPolygon(polys)    
    name=acmd['attributes']['Area_Command']    
    cursor.execute("INSERT INTO areacommand (name, geom) VALUES ('{}', ST_GeomFromText('{}'))".format(name, p.wkt))
connection.commit() 
 


url='http://coagisweb.cabq.gov/arcgis/rest/services/public/adminboundaries/MapServer/9/query' 
params={"where":"1=1","outFields":"*","outSR":"4326","f":"json"}
r=requests.get(url,params=params) 
data=r.json()
for acmd in data['features']:    
    polys=[]    
    for ring in acmd['geometry']['rings']:        
        polys.append(Polygon(ring))    
    p=MultiPolygon(polys)
    beat = acmd['attributes']['BEAT']    
    agency = acmd['attributes']['AGENCY']    
    areacomm = acmd['attributes']['AREA_COMMA']
    cursor.execute("INSERT INTO beats (beat, agency,areacomm,geom) VALUES ('{}','{}','{}', ST_GeomFromText('{}'))".format(beat,agency,areacomm,p.wkt))
connection.commit() 


url='http://coagisweb.cabq.gov/arcgis/rest/services/public/APD_Incidents/MapServer/0/query' 
params={"where":"1=1","outFields":"*","outSR":"4326","f":"json"} 
r=requests.get(url,params=params) 
data=r.json()
for a in data["features"]:    
    address=a["attributes"]["CV_BLOCK_ADD"]    
    crimetype=a["attributes"]["CVINC_TYPE"]    
    if a['attributes']['date'] is None:        
        pass    
        else:        
            date = datetime.datetime.fromtimestamp(a['attributes']['date'] / 1e3).date()    
        try:        
            p=Point(float(a["geometry"]["x"]),float(a["geometry"]["y"]))        
            cursor.execute("INSERT INTO incidents (address,crimetype,date, geom) VALUES ('{}','{}','{}', ST_GeomFromText('{}'))".format(address,crimetype,str(date), p.wkt))
        except KeyError:        
            pass
connection.commit()


import psycopg2 
from shapely.geometry 
import Point,Polygon,MultiPolygon
from shapely.wkb import loads 
from shapely.wkt import dumps, loads 
import datetime 
import json 
from ipyleaflet import ( Map, Marker, TileLayer, ImageOverlay, Polyline, Polygon, Rectangle, Circle, CircleMarker, GeoJSON ) 


connection = psycopg2.connect(database="pythonspatial",user="postgres", password="postgres") 
cursor = connection.cursor()
cursor.execute("SELECT name, ST_AsGeoJSON(geom) from areacommand") 
c=cursor.fetchall() 
c[0] 


center = [35.106196,-106.629515] 
zoom = 10
map = Map(center=center, zoom=zoom) 
map


for x in c:   
    layer=json.loads(x[1])   
    layergeojson=GeoJSON(data=layer)   
    map.add_layer(layergeojson)


cursor.execute("SELECT beat, ST_AsGeoJSON(geom) from beats") 
c=cursor.fetchall() 
for x in c:   
    layer=json.loads(x[1])   
    layergeojson=GeoJSON(data=layer)   
    map.add_layer(layergeojson)   

d=datetime.datetime.strptime('201781','%Y%m%d').date() 
cursor.execute("SELECT address,crimetype,date,ST_AsGeoJSON(geom) from incidents where date = '{}' ".format(str(d))) 
incidents_date=cursor.fetchall() 
for x in incidents_date:    
    layer=json.loads(x[3])    
    layergeojson=GeoJSON(data=layer)    
    map.add_layer(layergeojson) 

d=datetime.datetime.strptime('201781','%Y%m%d').date() 
cursor.execute("SELECT address,crimetype,date,ST_AsGeoJSON(geom) from incidents where date > '{}' ".format(str(d))) 

cursor.execute("select * from incidents where date >= NOW() - interval '10 day'") 

cursor.execute("SELECT ST_AsGeoJSON(i.geom) FROM incidents i JOIN areacommand acmd ON ST_Intersects(acmd.geom, i.geom) WHERE acmd.name like'FOOTHILLS' and date >= NOW() - interval '10 day';")
crime=cursor.fetchall() 
for x in crime:    
    layer=json.loads(x[0])    
    layergeojson=GeoJSON(data=layer)   
    map.add_layer(layergeojson)


cursor.execute("SELECT ST_AsGeoJSON(geom)from beats where beats.beat in ('336','523','117','226','638','636')")
c=cursor.fetchall() 
for x in c:    
    layer=json.loads(x[0])    
    layergeojson=GeoJSON(data=layer)    
    map.add_layer(layergeojson) 


cursor.execute("SELECT ST_AsGeoJSON(i.geom) FROM incidents i JOIN beats b ON ST_Intersects(b.geom, i.geom) WHERE b.beat in ('336','523','117','226','638','636') and date >= NOW() - interval '10 day';")
crime=cursor.fetchall() 
for x in crime:    
    layer=json.loads(x[0])    
    layergeojson=GeoJSON(data=layer)    
    map.add_layer(layergeojson)  


p = Point([-106.578677,35.062485]) 
pgeojson=mapping(p) 
player=GeoJSON(data=pgeojson) 
map.add_layer(player)


cursor.execute("SELECT ST_AsGeoJSON(ST_Buffer(ST_GeomFromText('{}')::geography,1500));".format(p.wkt)) 
buff=cursor.fetchall() 
buffer=json.loads(buff[0][0]) 
bufferlayer=GeoJSON(data=buffer) 
map.add_layer(bufferlayer) 


cursor.execute("SELECT ST_AsText(ST_Buffer(ST_GeomFromText('{}')::geography,1500));".format(p.wkt) ) 
bufferwkt=cursor.fetchall() 
b=loads(bufferwkt[0][0]) 

cursor.execute("SELECT ST_AsGeoJSON(incidents.geom) FROM incidents where ST_Intersects(ST_GeomFromText('{}'), incidents.geom) and date >= NOW() interval '10 day';".format(b.wkt)) 
crime=cursor.fetchall() 
for x in crime:    
    layer=json.loads(x[0])    
    layergeojson=GeoJSON(data=layer)    
    map.add_layer(layergeojson)


p = Point([-106.578677,35.062485]) 
cursor.execute("SELECT ST_AsGeoJSON(incidents.geom), ST_Distance(incidents.geom::geography,ST_GeometryFromText('{}')::geography) from incidents ORDER BY incidents.geom<->ST_GeometryFromText('{}') LIMIT 15".format(p.wkt,p.wkt)) 
c=cursor.fetchall() 
for x in c:    
    layer=json.loads(x[0])    
    layergeojson=GeoJSON(data=layer)    
    map.add_layer(layergeojson) 


from ipywidgets import interact, interactive, fixed, interact_manual,DatePicker 
import ipywidgets as widgets
@widgets.interact(x=DatePicker()) 
def theDate(x):
    if x:        
        for l in map.layers[1:]:        
        map.remove_layer(l)    
        nohyphen=str(x).replace("-","")    
        d=datetime.datetime.strptime(nohyphen,'%Y%m%d').date()    
        cursor.execute("SELECT ST_AsGeoJSON(geom) from incidents where date = '{}' ".format(str(d)))    
        c=cursor.fetchall()
    for x in c:        
        layer=json.loads(x[0])        
        layergeojson=GeoJSON(data=layer)        
        map.add_layer(layergeojson)    
    return len(c)
    else:        
        pass


@widgets.interact(x="None") 
def areaCommand(x):    
    if x:        
        for l in map.layers[1:]:            
            map.remove_layer(l)        
        cursor.execute("SELECT ST_AsGeoJSON(i.geom) FROM incidents i JOIN areacommand acmd ON ST_Intersects(acmd.geom, i.geom) WHERE acmd.name like'{}' and date >= NOW() - interval '10 day';".format(x))
        c=cursor.fetchall()
        for x in c:            
            layer=json.loads(x[0])            
            layergeojson=GeoJSON(data=layer)            
            map.add_layer(layergeojson)        
        return c    
    else:        
        pass 


import pandas as pd 
d=datetime.datetime.strptime('2017101','%Y%m%d').date() 
cursor.execute("SELECT date, count(date) from incidents where date > '{}' group by date".format(str(d))) 
df=pd.DataFrame(cursor.fetchall(),columns=["date","count"]) 
df.head() 


df.sort_values(by='date').plot(x="date",y="count",kind='bar',figsize=(15,10 )) 


cursor.execute("SELECT beats.beat, beats.agency, count(incidents.geom) as crimes from beats left join incidents on ST_Contains(beats.geom,incidents.geom) group by beats.beat, beats.agency") 
area=pd.DataFrame(cursor.fetchall(),columns=["Area","Agency","Crimes"]) 
area.head() 


area.plot(x="Area",y="Crimes",kind='bar',figsize=(25,10)) 


area[(area['Crimes']>800)].plot(x='Area',y='Crimes',kind='bar') 

query=('CREATE FUNCTION newcrime()'+'\n' 
'RETURNS trigger' +'\n' 
'AS $newcrime$' +'\n'
'BEGIN' +'\n' 
'IF NEW.crimetype IS NULL THEN'+'\n' 
'RAISE EXCEPTION' +" '% Must Include Crime Type', NEW.address;"+'\n' 
'END IF;'+'\n' 
'RETURN NEW;'+'\n' 
'END;'+'\n' 
'$newcrime$'+'\n' 
'LANGUAGE \'plpgsql\';' ) 
cursor.execute(query)


query=('CREATE TRIGGER newcrime BEFORE INSERT OR UPDATE ON incidents FOR EACH ROW EXECUTE PROCEDURE newcrime()') 
cursor.execute(query) 
connection.commit()


p=Point([-106,35]) 
address="123 Sesame St" 
cursor.execute("INSERT INTO incidents (address, geom) VALUES ('{}', ST_GeomFromText('{}'))".format(address, p.wkt)) 


