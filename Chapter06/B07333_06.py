from osgeo import gdal 

nmtif = gdal.Open(r'C:\Desktop\ColorRelief\nm_relief_color.tif') print(nmtif.GetMetadata()) 
nmtif.GetProjection() 

from osgeo import osr 
p=osr.SpatialReference() 
p.ImportFromEPSG(26913) 
nmtif.SetProjection(p.ExportToWkt()) 
nmtif.GetProjection()


geoTiffDriver="GTiff" 
driver=gdal.GetDriverByName(geoTiffDriver) 
out=driver.CreateCopy("copy.tif",nmtif,strict=0) 
out.GetProjection()

nmtif.RasterCount 
band=nmtif.GetRasterBand(1)
values=band.ReadAsArray()

 
one= nmtif.GetRasterBand(1).ReadAsArray() 
two = nmtif.GetRasterBand(2).ReadAsArray() 
three= nmtif.GetRasterBand(3).ReadAsArray() 
print(str(one[1100,1100])+","+ str(two[1100,1100])+","+str(three[1100,1100]))

one=nmtif.GetRasterBand(1) 
two=nmtif.GetRasterBand(2) 
three=nmtif.GetRasterBand(3) 
one.ComputeBandStats() 
two.ComputeBandStats() 
three.ComputeBandStats()

print(str(one.GetMinimum())+","+str(one.GetMaximum())) 


two.GetDescription()    # returns 'band_2' 
two.SetDescription("The Green Band") 
two.GetDescription()  # returns "The Green Band" 


import numpy as np 
from matplotlib.pyplot import imshow 
%matplotlib inline
data_array=nmtif.ReadAsArray() 
x=np.array(data_array[0]) # x.shape ---> 6652,6300 
w, h =6652, 6300 
image = x.reshape(x.shape[0],x.shape[1]) 
imshow(image, cmap='gist_earth')


a_raster=np.array([ [10,10,1,10,10,10,10], [1,1,1,50,10,10,50], [10,1,1,51,10,10,50], [1,1,1,1,50,10,50]]) 
coord=(-106.629773,35.105389) 
w=10
h=10 
name="BigI.tif"


d=gdal.GetDriverByName("GTiff") 
output=d.Create(name,a_raster.shape[1],a_raster.shape[0],1,gdal.GDT_UInt16) 
output.SetGeoTransform((coord[0],w,0,coord[1],0,h)) 
output.GetRasterBand(1).WriteArray(a_raster) 
outsr=osr.SpatialReference() 
outsr.ImportFromEPSG(4326) 
output.SetProjection(outsr.ExportToWkt()) 
output.FlushCache()

output.GetProjection() 

data=output.ReadAsArray() 
w, h =4, 7 
image = data.reshape(w,h) #assuming X[0] is of shape (400,) .T 
imshow(image, cmap='Blues') #enter bad color to get list 
data 


import psycopg2 
connection = psycopg2.connect(database="pythonspatial",user="postgres", password="postgres") 
cursor = connection.cursor()
cursor.execute("SELECT * from bigi") #Big I is the name of the intersection where I-25 and I-40 meet and split Albuquerque in quadrants. 
cursor.fetchall()

cursor.execute("select ST_Summary(rast) from bigi;") 
cursor.fetchall()


cursor.execute("select ST_MetaData(rast) from bigi") 
cursor.fetchall()

cursor.execute("select ST_AsText(ST_Envelope(rast)) from bigi;") 
cursor.fetchall()


cursor.execute("select st_height(rast), st_Width(rast) from bigi;") #st_width 
cursor.fetchall()

cursor.execute("select ST_PixelWidth(rast), ST_PixelHeight(rast) from bigi;") 
cursor.fetchall()

cursor.execute("select ST_SummaryStats(rast) from bigi;") 
cursor.fetchall()


cursor.execute("SELECT ST_Histogram(rast,1) from bigi;") 
cursor.fetchall() 

cursor.execute("select rid, ST_asText(ST_PixelAsPolygon(rast,7,2)) from bigi;") 
cursor.fetchall() 


cursor.execute("SELECT x, y, val, ST_AsText(geom) FROM (SELECT (ST_PixelAsPoints(rast, 1)).* FROM bigi) as foo;")
cursor.fetchall() 

cursor.execute("SELECT x, y, val, ST_AsText(geom) FROM (SELECT (ST_PixelAsCentroids(rast, 1)).* FROM bigi) as foo;")
cursor.fetchall()

cursor.execute("SELECT ST_AsText(ST_PixelAsCentroid(rast,4,1)) FROM bigi;") 
cursor.fetchall()


cursor.execute("select ST_Value(rast,4,3) from bigi;") 
cursor.fetchall()

cursor.execute("select ST_PixelOfValue(rast,1,50) from bigi;") 
cursor.fetchall()

cursor.execute("select ST_ValueCount(rast) from bigi;") 
cursor.fetchall()

cursor.execute("select ST_ValueCount(rast,1,True,50) from bigi;") 
cursor.fetchall()

cursor.execute("select ST_DumpValues(rast,1) from bigi;") 
cursor.fetchall()

cursor.execute("select ST_NearestValue(rast,( select ST_SetSRID( ST_MakePoint(-71.629773,60.105389),4326))) from bigi;".format(p.wkt))
cursor.fetchall() 

cursor.execute("select ST_Neighborhood(rast,(select ST_SetSRID( ST_MakePoint(410314,3469015),26913)),1,1) from newmexicoraster;")
cursor.fetchall() 

cursor.execute("SELECT ST_AsPNG(ST_asRaster(geom,150,250,'8BUI')) from areacommand where name like 'FOOTHILLS';")
c=cursor.fetchall()
with open('Foothills.png','wb') as f:    
    f.write(c[0][0]) 
    f.close()


   


 










