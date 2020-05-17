import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

app = Flask(__name__)

@app.route("/")
def home():
	return (
		f"Welcome.<br/>"
		f"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/stations<br/>"
		f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/<start><br/>"
		f"/api/v1.0/<start>/<end><br/>"
	)

@app.route("/api/v1.0/precipitation")
def precipitation():
    engine = create_engine("sqlite:///./Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    session = Session(engine)
    date_query = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date_split = date_query[0].split("-")
    print(date_split)
    last_date = dt.date(int(date_split[0]),int(date_split[1]), int(date_spit[2]))
    date_year_ago = last_date - dt.timedelta(days=365)
    precipitation_date = session.query(Measurement.date, Measurement.prcp).\
	    filter(Measurement.date > date_year_ago).order_by(Measurement.date.desc()).all()
    result_list = list()
    temp_dict = dict()
    for i in range(len(precipitation_date)):
    	temp_date = precipitation_date[i][0]
    	temp_prcp = precipitation_date[i][1]
    	temp_dict = {temp_date:temp_prcp}
    	result_list.append(temp_dict)
    session.close()
    return jsonify(result_list)

# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.


@app.route("/api/v1.0/stations")
def stations():
	engine = create_engine("sqlite:///./Resources/hawaii.sqlite")
	Base = automap_base()
	Base.prepare(engine, reflect=True)
	Station = Base.classes.station
	session = Session(engine)
	station_data = session.query(Station.station).distinct().all()
	station_list = list(np.ravel(station_data))
	session.close()
	return jsonify(station_list)
# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/tobs")
def tobs():
	engine = create_engine("sqlite:///./Resources/hawaii.sqlite")
	Base = automap_base()
	Base.prepare(engine, reflect=True)
	Station = Base.classes.station
	session = Session(engine)
	active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
	group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
	stat_station = session.query(Measurement.date, Measurement.tobs).\
	filter(Measurement.station == active_stations[0][0]).filter(Measurement.date > '2020-01-01').all()

	return
# Query the dates and temperature observations\
# of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/<start>")
def temp1(start):
	return

# Return a JSON list of the minimum temperature, the average temperature,\
# and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX \
# for all dates greater than and equal to the start date.

@app.route("/api/v1.0/<start>/<end>")
def temp2(start, end):
	return
# Return a JSON list of the minimum temperature, the average temperature,\
# and the max temperature for a given start or start-end range.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX\
# for dates between the start and end date inclusive.

if __name__ == "__main__":
	app.run(debug=True)