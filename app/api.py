from flask_restful import Api

from app.resources.station_resource import StationsResource
from app.resources.record_resource import RecordsResource
from app.resources.statistics_resource import StatisticRecordsResource, StatisticValueResource

api = Api()

api.add_resource(StationsResource, '/stations')
api.add_resource(RecordsResource, '/records')
api.add_resource(StatisticRecordsResource, '/statistic/records')
api.add_resource(StatisticValueResource, '/statistic/value')


