from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime

from app.service.record_service import get_statistical_record, get_statistical_value
from app.service.station_service import get_station_by_name


class StatisticRecordsResource(Resource):

    def get(self):
        params = request.args

        start_date = params.get('start_date')
        end_date = params.get('end_date')

        record, error = get_statistical_record(
            start_date=datetime.strptime(start_date, '%Y-%m-%d') if start_date is not None else None,
            end_date=datetime.strptime(end_date, '%Y-%m-%d') if end_date is not None else None,
            stat_type=params.get('stat_type'), parameter=params.get('parameter'),
            region=params.get('region'), province=params.get('province'),
            district=params.get('district'),
            station_name=params.get('station_name'))

        if record is not None and error == '':
            station = get_station_by_name(record.station_name)
            return jsonify({
                    'record': record.to_dict(),
                    'station': station.to_dict()
                })

        return {'message': error}, 400

class StatisticValueResource(Resource):
    def get(self):
        params = request.args

        start_date = params.get('start_date')
        end_date = params.get('end_date')

        value, error = get_statistical_value(
            start_date=datetime.strptime(start_date, '%Y-%m-%d') if start_date is not None else None,
            end_date=datetime.strptime(end_date, '%Y-%m-%d') if end_date is not None else None,
            stat_type=params.get('stat_type'), parameter=params.get('parameter'),
            region=params.get('region'), province=params.get('province'),
            district=params.get('district'),
            station_name=params.get('station_name'))

        if value is not None and error == '':
            return jsonify({
                'value': value
            })

        return {'message': error}, 400
