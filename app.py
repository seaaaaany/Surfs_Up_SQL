import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurements
Station = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


# home
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )


# return precipitation data for previous year
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago).all()
    recent_prcp_json = jsonify(dict(results))
    return recent_prcp_json

# return a json list of stations from the dataset.


@app.route("/api/v1.0/stations")
def stations():
    results_1 = session.query(Measurement.station, func.count(Measurement.tobs))\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.tobs).desc()).all()
    station_list_json = jsonify(results_1)
    return station_list_json

# return a json list of Temperature Observations (tobs) for the previous year


@app.route("/api/v1.0/tobs")
def tobs():
    recent_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > year_ago).all()
    recent_tobs_json = jsonify(dict(recent_tobs))
    return recent_tobs_json

# return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# cannot get these to run


@app.route("/api/v1.0/<string:start>")
def start(start):

    date = datetime.strptime(start, '%Y-%m-%d')

    minimum = session.query(func.min(Measurement.tobs)).filter(Measurement.date > start).all()
    maximum = session.query(func.max(Measurement.tobs)).filter(Measurement.date > start).all()
    average = session.query(func.avg(Measurement.tobs)).filter(Measurement.date > start).all()

    temp_dict = {'min': minimum, 'max': maximum, 'avg': average}

    return jsonify(temp_dict)


@app.route("/api/v1.0/<string:start>/<string:end>")
def startend(start, end):

    minimum = session.query(func.min(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date > end).all()
    maximum = session.query(func.max(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date > end).all()
    average = session.query(func.avg(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date > end).all()

    # create dict
    temp_dict = {'min': minimum, 'max': maximum, 'avg': average, 'start': start, 'end': end}

    # return jsonify
    return jsonify(temp_dict)


if __name__ == "__main__":
    app.run()
