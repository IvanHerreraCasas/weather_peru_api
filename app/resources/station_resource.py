from flask import request, jsonify
from flask_restful import Resource
from app.service.station_service import save_station, get_available_stations


class StationsResource(Resource):

    endpoint = 'stations'
    def get(self):
        data = request.form

        region = data.get('region')
        province = data.get('province')
        district = data.get('district')

        stations = get_available_stations(region, province, district)

        stations_dict = []

        for station in stations:
            stations_dict.append(station.to_dict())

        return jsonify(stations_dict)

    def post(self):
        data = request.form

        station = save_station(data)

        return {'message': 'Station saved successfully.', 'station': station.to_dict()}, 200
