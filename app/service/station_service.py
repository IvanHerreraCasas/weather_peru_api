from sqlalchemy import and_

from app.database import db
from app.models import Station


def save_station(data):
    name = data.get('name')
    region = data.get('region')
    province = data.get('province')
    district = data.get('district')

    station = db.session.query(Station).filter_by(name=name).first()

    if station:
        station.region = region
        station.province = province
        station.district = district
        db.session.commit()
        return station

    station = Station(name=name, region=region, province=province, district=district)
    db.session.add(station)
    db.session.commit()

    return station


def get_station(station_id):
    station = db.get_or_404(Station, station_id)

    return station


def get_station_by_name(name):
    station = db.session.query(Station).filter_by(name=name).first()

    return station


def get_available_stations(region, province, district):
    filters = []

    if region is not None:
        filters.append(Station.region == region)

    if province is not None:
        filters.append(Station.province == province)

    if district is not None:
        filters.append(Station.district == district)

    stations = db.session.query(Station).where(and_(*filters)).all()

    return stations
