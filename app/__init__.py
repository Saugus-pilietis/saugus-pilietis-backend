import os
from flask import Flask
from flask_influxdb import InfluxDB

import api.keys.controller

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', "NOT_DEFINED")

if GOOGLE_API_KEY == "NOT_DEFINED":
    print("Please put your Google API key in the environment variables!")
    quit()



db = InfluxDB()

def initialize_config_from_env(app):
    app.config["INFLUXDB_HOST"] = os.getenv("INFLUXDB_HOST")
    app.config["INFLUXDB_PORT"] = os.getenv("INFLUXDB_PORT")
    app.config["INFLUXDB_USER"] = os.getenv("INFLUXDB_USER")
    app.config["INFLUXDB_PASS"] = os.getenv("INFLUXDB_PASS")
    
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    
    app.config["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def create_app():
    app = Flask(__name__)
    db.init_app(app)

    initialize_config_from_env(app)

    with app.app_context():
        app.register_blueprint(api.keys.controller.keys, url_prefix='/api/keys')

    return app
