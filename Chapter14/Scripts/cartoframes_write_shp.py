import geopandas as gdp
import cartoframes
APIKEY = "1353407a098fef50ec1b6324c437d6d52617b890"

cc = cartoframes.CartoContext(base_url='https://lokiintelligent.carto.com/',
                              api_key=APIKEY)

shp = r"C:\Data\Stadiums_MLB\Stadiums_MLB.shp"
data = gdp.read_file(shp)
cc.write(data,"stadiums_mlb")