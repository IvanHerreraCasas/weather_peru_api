from flask_restful import Api

from app.resources.station_resource import StationsResource
from app.resources.record_resource import RecordsResource

api = Api()

api.add_resource(StationsResource, '/stations')
api.add_resource(RecordsResource, '/records/<station_id>')


