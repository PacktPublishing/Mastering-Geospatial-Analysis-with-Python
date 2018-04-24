import requests 
import json 
from qgis.core import * 
from qgis.PyQt.QtGui import * 
from qgis.PyQt.QtWidgets 
import * 
from qgis.PyQt.QtCore import * 

streets = QgsVectorLayer(r'C:\Users\Paul\Desktop\PythonBook\CHP8\Streets.shp', "Streets","ogr") 
scf = QgsVectorLayer(r'C:\Users\Paul\Desktop\PythonBook\CHP8\SCF.shp', "SeeClickFix","ogr")
QgsMapLayerRegistry.instance().addMapLayers([scf,streets]) 

streets = iface.addVectorLayer(r'C:\Users\Paul\Desktop\PythonBook\CHP8\Streets.shp', "Streets","ogr") 
scf = iface.addVectorLayer(r'C:\Users\Paul\Desktop\PythonBook\CHP8\SCF.shp', "SeeClickFix","ogr")  
QgsMapLayerRegistry.instance().mapLayers() 

QgsMapLayerRegistry.instance().removeMapLayer('Streets20171129100433367')

QgsMapLayerRegistry.instance().removeMapLayer(streets.id()) 

crs = scf.crs() 
crs.description()
crs.toWkt()

extent = scf.extent()  
extent.toString() 
extent.asWktPolygon() 
extent.xMinimum() 
extent.xMaximum() 
extent.yMinimum() 
extent.yMaximum() 

scf.pendingFeatureCount() 

item=scf.getFeatures().next() 

g = item.geometry() 
g.type() 

item.geometry().asPoint() #(-106.652,35.0912)
item.geometry().asPoint()[0] #-106.65153503418
item.geometry().asPoint()[1] #35.0912475585134  

street = streets.getFeatures().next().geometry().type()


street.geometry().asPolyline() 

item.fields().count() 

item.fields()[2].name() 
item.fields()[2].typeName()

item["Type"]
item[0]
item[1]
item[2]
item[3] 

for f in scf.getFeatures():
if f["Status"]=='Closed':        
    print(f["ID"]) 

theLayer=QgsVectorLayer('Point?crs=epsg:4326','SomePoints','memory') 

from qgis.PyQt.QtCore import * 
theFeatures=theLayer.dataProvider() 
theFeatures.addAttributes([QgsField("ID", QVariant.Int),QgsField("Name", Qvariant.String)]) 


p=QgsFeature() 
point=QgsPoint(-106.3463,34.9685) 
p.setGeometry(QgsGeometry.fromPoint(point)) 
p.setAttributes([123,"Paul"]) 
theFeatures.addFeatures([p]) 
theLayer.updateExtents() 
theLayer.updateFields()

QgsMapLayerRegistry.instance().addMapLayers([theLayer]) 

import psycopg2 
connection = psycopg2.connect(database="pythonspatial",user="postgres", password="postgres") 
cursor = connection.cursor() 
cursor.execute("SELECT name, ST_AsTexT(geom) from areacommand")
c=cursor.fetchall()


APD=QgsVectorLayer('Polygon?crs=epsg:4326','AreaCommands','memory') 
APDfeatures=APD.dataProvider() 
APDfeatures.addAttributes([QgsField("ID",QVariant.Int),QgsField("Name", QVariant.String)]) 
x=0  

for acmd in c:   
    g=QgsGeometry()    
    g=QgsGeometry.fromWkt(acmd[1])    
    p=QgsFeature()    
    print(acmd[0])    
    p.setGeometry(g)    
    x+=1    
    p.setAttributes([x,str(acmd[0])])    
    APDfeatures.addFeatures([p])    
    APD.updateExtents()    
    APD.updateFields() 


QgsMapLayerRegistry.instance().addMapLayers([APD]) 

scf = iface.addVectorLayer(r'C:\Users\Paul\Desktop\PythonBook\CHP8\SCF.shp', "SeeClickFix","ogr") 

scf.dataProvider().capabilitiesString()

feat = QgsFeature(scf.pendingFields()) 
feat.setAttribute('fid',911) 
feat.setAttribute('ID',311) 
feat.setAttribute('Type','Pothole') 
feat.setAttribute('Status','Pending') 
feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(-106.65897,35.07743))) 
scf.dataProvider().addFeatures([feat]) 


feat.setAttributes([912,312,"Other","Closed"]) 

for x in scf.getFeatures():    
    if x["ID"]==311:    
         scf.dataProvider().deleteFeatures([x.id()])

for x in scf.getFeatures():    
    if x["Status"]=='Closed':        
        key.append(x.id()) 
    scf.dataProvider().deleteFeatures(key)

scf.dataProvider().changeAttributeValues({114:{0:123,1:345,2:"ADA",3:"NEW"} }) 

attributes={3:"Closed"} 
for x in scf.getFeatures(): 
    if x["Type"]=='Other': 
        scf.dataProvider().changeAttributeValues({x.id():attributes})  


from qgis.PyQt.QtGui import * 
from qgis.PyQt.QtWidgets import * 
iface.mapCanvas().setSelectionColor( QColor("red") ) 
scf.setSelectedFeatures([100]) 

closed=[] 
exp=QgsExpression("Type='Traffic Signs' and Status='Acknowledged'") 
exp.prepare(scf.pendingFields()) 
for f in scf.getFeatures():    
    if exp.evaluate(f)==1:    
        closed.append(f.id()) 
scf.setSelectedFeatures(closed)



import processing 
processing.alglist() 

processing.alglist(“buffer”)

processing.alghelp("gdalogr:buffervectors") 

processing.runalg("gdalogr:buffervectors",r'C:/Users/Paul/Desktop/Projected. shp',"geometry",100,False,None,False,"",r'C:/Users/Paul/Desktop/ProjectedBuffer.shp') 
layer = iface.addVectorLayer(r'C:\Users\Paul\Desktop\ProjectedBuffer.shp', "Buffer", "ogr") 



scfcity=City_or_Neighborhood 
searchterm=Filter 
progress.setInfo("Wait while I get data from the API") 
progress.setText("Calling API") 
if searchterm=="None": 
    pagesURL="http://seeclickfix.com/api/v2/issues?per_page=100&place_url="+scf city+"&page=" 
    url="http://seeclickfix.com/api/v2/issues?per_page=100&place_url="+scfcity 
else: 
    pagesURL="http://seeclickfix.com/api/v2/issuesper_page=100&place_url="+scfc ity+"&search="+searchterm+"&page="
    url="http://seeclickfix.com/api/v2/issues?per_page=100&search="+searchterm+"&place_url="+scfcity 


crs=QgsCoordinateReferenceSystem("epsg:4326") 
scf=QgsVectorLayer('Point?crs=epsg:4326','SeeClickFix','memory')
fields = QgsFields() 
fields.append(QgsField("ID", QVariant.Int)) 
fields.append(QgsField("Type", QVariant.String)) 
fields.append(QgsField("Status", QVariant.String))
writer = processing.VectorWriter(Output, None, fields.toList(), QGis.WKBPoint, crs)


r = requests.get(url).text 
rJSON=json.loads(r) 
pages=rJSON['metadata']['pagination']['pages'] 
records=rJSON['metadata']['pagination']['entries'] 
progress.setInfo("Grabbing "+str(records) +" Records") 
count=1
for x in range(1,pages+1):    
    progress.setText("Reading page "+str(x))    
    pageData=requests.get(pagesURL+str(x)).text    
    pageDataJSON=json.loads(pageData)


for issue in pageDataJSON['issues']:
    try:    
        p=QgsFeature()    
        point=QgsPoint(issue['lng'],issue['lat'])    
        p.setGeometry(QgsGeometry.fromPoint(point)) 
        p.setAttributes([issue["id"],issue["request_type"]["title"],issue["status"]	])    
        writer.addFeature(p)    
        progress.setPercentage((count/float(records))*100)    
        count+=1 
    except:    
        pass

del writer 


processing.alghelp("script:seeclickfix")

out=processing.runalg("script:seeclickfix","Albuquerque","Juan Tabo",None) 
out










