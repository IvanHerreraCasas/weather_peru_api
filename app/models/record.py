from app.database import db


class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    precipitation = db.Column(db.Float, nullable=True)
    min_temp = db.Column(db.Float, nullable=True)
    max_temp = db.Column(db.Float, nullable=True)
    station_name = db.Column(db.String(30), db.ForeignKey('stations.name'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%Y-%m-%d'),
            'precipitation': self.precipitation,
            'max_temp': self.max_temp,
            'min_temp': self.min_temp,
            'station_name': self.station_name
        }
