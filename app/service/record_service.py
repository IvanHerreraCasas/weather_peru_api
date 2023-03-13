import os

from flask import current_app
from datetime import date
from sqlalchemy import select, func, Select

from typing import Optional, List

from app.database import db
from app.models import Record

from app.service.station_service import get_station_by_name, get_available_stations


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
                station_name=station.name
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


def get_records(record_id: int = None, start_date: date = None, end_date: date = None,
                parameter: str = None, region: str = None, province: str = None,
                district: str = None, station_name: str = None) -> List[Record]:
    if record_id is not None:
        stmt = select(Record).where(Record.id == record_id)
    else:
        stmt = create_select_stmt(Record, start_date, end_date, parameter, region, province, district, station_name)

    records = db.session.execute(stmt).scalars()
    return records


def get_statistical_record(start_date: date = None, end_date: date = None,
                           stat_type: str = None, parameter: str = None,
                           region: str = None, province: str = None,
                           district: str = None, station_name: str = None) \
        -> tuple[Optional[List[Record]], str]:
    if parameter not in ["max_temp", "min_temp", "precipitation"]:
        return None, "Parameter can only be max_temp, min_temp or precipitation"

    if stat_type not in ["max", "min"]:
        return None, "Statistical type can only be max or min"

    if station_name is not None:
        station = get_station_by_name(station_name)
        if station is None:
            return None, f"{station_name} station does not exist"

    record_column = get_record_column_from_parameter(parameter)

    record: Optional[Record] = None

    stmt = create_select_stmt(Record, start_date, end_date, parameter, region, province, district, station_name)

    if stat_type == "max":
        stmt = stmt.order_by(record_column.desc())
    elif stat_type == "min":
        stmt = stmt.order_by(record_column.asc())

    record = db.session.execute(stmt).scalar()

    return record, ''


def get_statistical_value(start_date: date = None, end_date: date = None,
                          stat_type: str = None, parameter: str = None,
                          region: str = None, province: str = None,
                          district: str = None, station_name: str = None) \
        -> tuple[Optional[int], str]:
    if parameter not in ["max_temp", "min_temp", "precipitation"]:
        return None, "Parameter can only be max_temp, min_temp or precipitation"

    if stat_type not in ["average"]:
        return None, "Statistical type can only be average"

    if station_name is not None:
        station = get_station_by_name(station_name)
        if station is None:
            return None, f"{station_name} station does not exist"

    record_column = get_record_column_from_parameter(parameter)

    stmt = None

    if stat_type == "average":
        stmt = create_select_stmt(func.avg(record_column),
                                  start_date,
                                  end_date,
                                  parameter,
                                  region,
                                  province,
                                  district,
                                  station_name)

    value = db.session.execute(stmt).scalar()

    return value, ''


def create_select_stmt(selectable=Record, start_date: date = None,
                       end_date: date = None, parameter: str = None,
                       region: str = None, province: str = None,
                       district: str = None, station_name: str = None) -> Select:
    if start_date is None:
        start_date = date(1950, 1, 1)

    if end_date is None:
        end_date = date(2050, 1, 1)

    station_names: list[str] = []

    if station_name is not None:
        station_names.append(station_name)
    else:
        stations = get_available_stations(region, province, district)
        for station in stations:
            station_names.append(station.name)

    stmt = select(selectable) \
        .where(Record.station_name.in_(station_names)) \
        .where(Record.date >= start_date) \
        .where(Record.date <= end_date)

    record_column = get_record_column_from_parameter(parameter)

    if record_column is not None:
        stmt = stmt.where(record_column.isnot(None))
    return stmt


def get_record_column_from_parameter(parameter: str):
    if parameter == "max_temp":
        return Record.max_temp
    elif parameter == "min_temp":
        return Record.min_temp
    elif parameter == "precipitation":
        return Record.precipitation
