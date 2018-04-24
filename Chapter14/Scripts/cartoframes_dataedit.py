import geopandas as gdp
import cartoframes
import pandas as pd
APIKEY = "1353407a098fef50ec1b6324c437d6d52617b890"

cc = cartoframes.CartoContext(base_url='https://lokiintelligent.carto.com/',
							  api_key=APIKEY)
from shapely.geometry import Point
from shapely.wkb import loads
arenas_df = cc.read('arenas_nba')
shp = r"C:\Data\US_States\US_States.shp"
states_df = gdp.read_file(shp)
data = []
for index, ref in arenas_df.iterrows():
	check = 0
	for index2, orig in states_df.iterrows():

		if loads(ref['the_geom'], hex=True).intersects(orig['geometry']):
			print(orig['STATE'], ref['team'])
			data.append(orig['STATE'])
			check = 1
	if check == 0:
		data.append(None)
arenas_df['state'] = data
cc.write(arenas_df,'arenas_nba', overwrite=True)