token = 'sk.eyJ1IjoibG9oxZGdqIn0.Y-qlJfzFzr3MGkOPPbtZ5g'
from mapbox import Uploader
import uuid
set_id = uuid.uuid4().hex
service = Uploader(access_token=token)
with open('ztca_bayarea.geojson', 'rb') as src:
    response = service.upload(src, set_id)
print(response)