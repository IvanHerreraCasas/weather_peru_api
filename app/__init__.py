from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevelopmentConfig
from app.resources.station import StationListResource

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)

from app.models.station import Station

migrate = Migrate(app, db)

api = Api(app)

api.add_resource(StationListResource, '/stations/<city>')

if __name__ == '__main__':
    app.run()