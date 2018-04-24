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

# for index, arena in arenas_df.iterrows():
# 	print(arena['the_geom'])
# 	arenas_df.at[index, 'the_geom'] = loads(arena.the_geom, hex=True)
# 	print(arenas_df.at[index, 'the_geom'])
data=[]



for index, orig in states_df.iterrows():
    for index2, ref in arenas_df.iterrows():

    	if loads(ref['the_geom'], hex=True).intersects(orig['geometry']):
        	print(orig['STATE'], ref['team'])