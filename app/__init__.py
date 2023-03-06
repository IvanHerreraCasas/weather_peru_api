from flask import Flask
from flask_restful import Api
from config import DevelopmentConfig
from app.resources.station import StationListResource

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

api = Api(app)

if __name__ == '__main__':
    app.run()
