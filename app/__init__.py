import os
from flask import Flask
from flask_influxdb import InfluxDB
from flask_cors import CORS

import api.keys.controller
import api.air_quality.controller

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', "NOT_DEFINED")

if GOOGLE_API_KEY == "NOT_DEFINED":
    print("Please put your Google API key in the environment variables!")
    quit()




def initialize_config_from_env(app):
    app.config["INFLUXDB_HOST"] = os.getenv("INFLUXDB_HOST")
    app.config["INFLUXDB_PORT"] = os.getenv("INFLUXDB_PORT")
    app.config["INFLUXDB_USER"] = os.getenv("INFLUXDB_USER")
    app.config["INFLUXDB_PASSWORD"] = os.getenv("INFLUXDB_PASS")
    
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    
    app.config["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def create_app():
    app = Flask(__name__)
    initialize_config_from_env(app)

    db = InfluxDB(app)
    with app.app_context():
        db.connect()
        db.connection.switch_database(database="sauguspilietis")
    CORS(app)

    app.config["db"] = db

    with app.app_context():
        app.register_blueprint(api.keys.controller.keys, url_prefix='/api/keys')
        app.register_blueprint(api.air_quality.controller.airQuality, url_prefix='/api/airQuality')
    return app
