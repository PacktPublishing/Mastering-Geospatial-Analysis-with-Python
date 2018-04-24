import cartoframes

APIKEY = "1353407a098fef50ec1b6324c437d6d52617b890"



# `base_url`s are of the form `http://{username}.carto.com/` for most users
cc = cartoframes.CartoContext(base_url='https://lokiintelligent.carto.com/',
                              api_key=APIKEY)

# read a table from your CARTO account to a DataFrame
df = cc.read('arenas_nba')

