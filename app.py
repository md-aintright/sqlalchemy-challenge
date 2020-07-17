from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import datetime as dt

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################

# Create an app
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define static routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App Homepage<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    prcp_result = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    prcp_list = []
    for date, prcp in prcp_result:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        prcp_list.append(prcp_dict)
    
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations_results = session.query(Station.station).all()

    session.close()

    # Convert tuple list to normal list
    stations_list = list(np.ravel(stations_results))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # date of last data point for top station is 2017-08-18 based on queries performed in climate_starter.ipynb
    query_date = dt.date(2017, 8, 18) - dt.timedelta(days=365)

    # USC00519281 is the most active station based on queries performed in climate_starter.ipynb
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station=='USC00519281').\
    filter(Measurement.date >= query_date).all()

    session.close()

    tobs_list = list(np.ravel(tobs_results))
    
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    temp_list = list(np.ravel(temp_results))
    
    return jsonify(temp_list) 

@app.route("/api/v1.0/<start>/<end>")
def startEnd(start, end):
    session = Session(engine)
    
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    temp_list = list(np.ravel(temp_results))
    
    return jsonify(temp_list) 

# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
