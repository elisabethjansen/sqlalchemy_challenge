# Import the dependencies.
import numpy as np
import datetime as dt
from datetime import timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of last 12 month precipitation data"""
    # Query last 12 months
    precip_results = session.query(Measurement.prcp, Measurement.date).\
        filter(Measurement.date <= dt.date(2017, 8, 23), Measurement.date >= dt.date(2016, 8, 23)).all()

    session.close()


    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for prcp, date in precip_results:
        precip_dict = {}
        precip_dict["prcp"] = prcp
        precip_dict["date"] = date
        all_precipitation.append(precip_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(func.distinct(Measurement.station)).all()

    session.close()

    # list to hold results
    all_stations = [result[0] for result in results]

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all temperature observations"""
    # Query all observations
    results = session.query(Measurement.tobs, Measurement.date).\
        filter(Measurement.station == 'USC00519281', Measurement.date <= dt.date(2017, 8, 23), Measurement.date >= dt.date(2016, 8, 23)).all()

    session.close()

    #create list to hold results
    active_station = []
    for tobs, date in results:
        active_dict = {}
        active_dict["tobs"] = tobs
        active_dict["date"] = date
        active_station.append(active_dict)

    return jsonify(active_station)

@app.route("/api/v1.0/<start>")
def start_date(start):
    """Fetch the max, min, avg temp for date specified"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query measurement for date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    # Store temp data
    temp_data = []
    for min_temp, avg_temp, max_temp in results:
        temp_data.append({
            "Min Temperature": min_temp,
            "Average Temperature": avg_temp,
            "Max Temperature": max_temp})
        
    return jsonify(temp_data)
    
@app.route("/api/v1.0/<start>/<end>")
def date_range(start,end):
    """Fetch the max, min, avg temp for dates specified."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query measurement for date range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()

    session.close()

    # Store temp data
    temp_data = []
    for min_temp, avg_temp, max_temp in results:
        temp_data.append({
            "Min Temperature": min_temp,
            "Average Temperature": avg_temp,
            "Max Temperature": max_temp})
        
    return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)










