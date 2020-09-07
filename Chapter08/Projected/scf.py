import requests
import json
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtCore import *

crs=QgsCoordinateReferenceSystem("epsg:4326")
scf=QgsVectorLayer('Point?crs=epsg:4326','SeeClickFix','memory')
scfeatures=scf.dataProvider()
scfeatures.addAttributes([QgsField("ID", QVariant.Int),QgsField("Type", QVariant.String),QgsField("Status", QVariant.String)])

url="http://seeclickfix.com/api/v2/issues?place_url=albuquerque&per_page=100"
r = requests.get(url).text
rJSON=json.loads(r)
pages=rJSON['metadata']['pagination']['pages']
pagesURL="http://seeclickfix.com/api/v2/issues?place_url=albuquerque&per_page=100&page="


for x in range(1,pages+1):
    pageData=requests.get(pagesURL+str(x)).text
    pageDataJSON=json.loads(pageData)
    
    for issue in pageDataJSON['issues']:
        try:
            
            p=QgsFeature()
            point=QgsPoint(issue['lng'],issue['lat'])
            
            p.setGeometry(QgsGeometry.fromPoint(point))
            p.setAttributes([issue["id"],issue["request_type"]["title"],issue["status"]])
            scfeatures.addFeatures([p])
            scf.updateExtents()
            scf.updateFields()
            #issues.append([issue["acknowledged_at"],issue["address"],issue["closed_at"],issue["comment_url"],issue["created_at"],issue["description"],issue["flag_url"],issue["html_url"],issue["id"],issue["lat"],issue["lng"],issue["media"]["image_full"],issue["media"]["image_square_100x100"],issue["media"]["representative_image_url"],issue["media"]["video_url"],issue["rating"],issue["reopened_at"],issue["reporter"]["avatar"]["full"],issue["reporter"]["avatar"]["square_100x100"],issue["reporter"]["civic_points"],issue["reporter"]["id"],issue["reporter"]["name"],issue["reporter"]["role"],issue["request_type"]["id"],issue["request_type"]["related_issues_url"],issue["request_type"]["title"],issue["request_type"]["url"],issue["shortened_url"],issue["status"],issue["summary"],issue["updated_at"],issue["url"]])
        except:
            pass



QgsMapLayerRegistry.instance().addMapLayers([scf])
QgsVectorFileWriter.writeAsVectorFormat(scf, r'C:\Users\Paul\Desktop\SCF.gpkg', "UTF-8", crs , "GPKG")