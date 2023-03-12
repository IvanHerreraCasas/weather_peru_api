from flask import Flask
from flask_migrate import Migrate
from config import DevelopmentConfig
from app.database import db
from app.api import api


def create_app(config=DevelopmentConfig):
    application = Flask(__name__)
    application.config.from_object(config)

    migrate = Migrate(application, db)

    db.init_app(application)
    migrate.init_app(application)

    api.init_app(application)

    return application

