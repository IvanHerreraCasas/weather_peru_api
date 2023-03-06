from flask_restful import Resource
from ..resources import get_available_stations


class StationListResource(Resource):
    def get(self, city):

        return get_available_stations(city)

