import geopandas as gdp
import cartoframes
import pandas as pd
APIKEY = "1353407a098fef50ec1b6324c437d6d52617b890"

cc = cartoframes.CartoContext(base_url='https://lokiintelligent.carto.com/',
                              api_key=APIKEY)
from shapely.geometry import Point
address_df = pd.read_csv(r'C:\Data\us\ak\city_of_juneau.csv')
geometry = [Point(xy) for xy in zip(address_df.LON, address_df.LAT)]
address_df = address_df.drop(['LON', 'LAT'], axis=1)
crs = {'init': 'epsg:4326'}
geo_df = gdp.GeoDataFrame(address_df, crs=crs, geometry=geometry)
cc.write(geo_df, 'juneau_addresses')