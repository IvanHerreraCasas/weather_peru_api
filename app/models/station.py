from app.database import db


class Station(db.Model):
    __tablename__ = 'stations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    region = db.Column(db.String(30), nullable=False)
    province = db.Column(db.String(30), nullable=False)
    district = db.Column(db.String(30), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'region': self.region,
            'province': self.province,
            'district': self.district
        }
