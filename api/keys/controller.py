from flask import Blueprint, jsonify, request
from flask import current_app as app
import os

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', "NOT_DEFINED")

keys = Blueprint('keys', __name__)

@keys.route("/map_key", methods=['GET'])
def get_map_key():
    return jsonify({
            'api_key': app.config["GOOGLE_API_KEY"]
            })
