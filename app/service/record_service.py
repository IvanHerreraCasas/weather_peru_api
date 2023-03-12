import os

from flask import current_app
from datetime import date

from app.database import db
from app.models import Record


def save_records_from_file(station, path):
    records = []
    with open(path, 'r') as f:
        for line in f:
            values = line.strip().split()
            year, month, day, precipitation, max_temp, min_temp = values
            if float(precipitation) == -99.9:
                precipitation = None
            if float(max_temp) == -99.9:
                max_temp = None
            if float(min_temp) == -99.9:
                min_temp = None
            record = Record(
                date=date(int(year), int(month), int(day)),
                precipitation=precipitation,
                max_temp=max_temp,
                min_temp=min_temp,
                station_id=station.id
            )
            records.append(record)
    save_records(records)


def save_records_file(name, file_contents):
    folder = current_app.config['UPLOAD_FOLDER']

    os.makedirs(folder, exist_ok=True)

    new_filename = f'{name}.txt'

    path = os.path.join(folder, new_filename)

    with open(os.path.join(folder, new_filename), 'wb') as new_file:
        new_file.write(file_contents)

    return path


def save_records(records):
    db.session.bulk_save_objects(records)
    db.session.commit()
