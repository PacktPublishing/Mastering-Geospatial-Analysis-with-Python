import cartoframes
import pandas as pd
APIKEY = "1353407a098fef50ec1b6324c437d6d52617b890"

cc = cartoframes.CartoContext(base_url='https://lokiintelligent.carto.com/',
                              api_key=APIKEY)
df = pd.read_csv(r'sacramento.csv')
cc.write(df, 'sacramento_addresses')