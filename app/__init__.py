import os
from flask import Flask
from flask_influxdb import InfluxDB
from flask_cors import CORS

import api.keys.controller

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', "NOT_DEFINED")

if GOOGLE_API_KEY == "NOT_DEFINED":
    print("Please put your Google API key in the environment variables!")
    quit()

db = InfluxDB()

def create_app():
    app = Flask(__name__)

    db.init_app(app)
    CORS(app)

    app.config['GOOGLE_API_KEY'] = GOOGLE_API_KEY

    with app.app_context():
        app.register_blueprint(api.keys.controller.keys, url_prefix='/api/keys')

    return app
