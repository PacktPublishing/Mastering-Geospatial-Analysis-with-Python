from mapbox import Datasets
import json
datasets = Datasets(access_token='sk.eyJ1IjoibG9raXByJjamc4aGRpZ3oyM3BxMzNuNWIzaDdja2ZzIn0.oFqNkH9Mlyv3ExsGknvSGg')
create_resp = datasets.create(name="Bay Area Zips", 
              description = "ZTCA zones for the Bay Area")
listing_resp = datasets.list()
dataset_id = [ds['id'] for ds in listing_resp.json()][0]
data = json.load(open(r'ztca_bayarea.geojson'))
for count,feature in enumerate(data['features'][:1]):
    resp = datasets.update_feature(dataset_id, count, feature)
