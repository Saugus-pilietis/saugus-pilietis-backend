from flask import Blueprint, request, jsonify
from flask import current_app as app

airQuality = Blueprint("airQuality", __name__)

@airQuality.route("/stations", methods=["GET"])
def stations():
    db = app.config["db"].connection
    db.switch_database("sauguspilietis")

    res = db.query("SHOW TAG VALUES WITH KEY IN (\"id\")")
    
    ids = []

    for measurement, tags in res.keys():
        for point in res.get_points(measurement=measurement, tags=tags):
            ids.append(point["value"])

    stations = {}

    for idx in ids:
        res = db.query("SHOW TAG VALUES WITH KEY IN (\"location\", \"name\", \"url\") WHERE \"id\"='%s'" % idx)
        stations[idx] = {}
        for measurement, tags in res.keys():
            for point in res.get_points(measurement=measurement, tags=tags):
                stations[idx][point["key"]] = point["value"] 
    return jsonify(stations)

@airQuality.route("/measurements", methods=["GET"])
def measurements():
    db = app.config["db"].connection
    db.switch_database("sauguspilietis")

    res = db.query("SELECT LAST(*) FROM airQuality GROUP BY id")
   
    measurement_data = {}

    for measurement, tags in res.keys():
        for point in res.get_points(measurement=measurement, tags=tags):
            measurement_data[tags['id']] = point

    return jsonify(measurement_data)

@airQuality.route("/historical_measurements/<station_id>", methods=["GET"])
def historical_measurements(station_id):
    db = app.config["db"].connection
    db.switch_database("sauguspilietis")

    res = db.query("SELECT * FROM airQuality WHERE id='%s' and time > now() - 6h GROUP BY id ORDER BY time asc" % station_id)

    measurement_data = {}

    for measurement, tags in res.keys():
        measurement_data[tags['id']] = []
        for point in res.get_points(measurement=measurement, tags=tags):
            measurement_data[tags['id']].append(point)

    return jsonify(measurement_data)
