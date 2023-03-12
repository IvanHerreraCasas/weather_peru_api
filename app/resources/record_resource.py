from flask import request
from flask_restful import Resource
from app.service.station_service import get_station
from app.service.record_service import save_records_from_file, save_records_file

import magic


class RecordsResource(Resource):

    def post(self, station_id):
        print(request.files.get('file'))

        file = request.files.get('file')
        if file is None:
            return {'message': 'No file uploaded.'}, 400

        file_contents = file.read()

        # validate file type
        file_type = magic.from_buffer(file_contents, mime=True)
        if not file_type == 'text/plain':
            return {'message': 'Invalid file type. Only text files are allowed.'}, 400

        station = get_station(station_id)

        # save file records
        path = save_records_file(station.name, file_contents)

        # save records
        save_records_from_file(station, path)

        return {'message': 'File saved successfully'}, 400
