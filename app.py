#IMPORTS
import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#___________________________________________________________

#DATABASE SETUP
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread':False})

#REFLECT
base = automap_base()
base.prepare(engine, reflect=True)

#SAVE REFERENCES
measurement = base.classes.measurement
station = base.classes.station

#CREATE SESSION LINK
session = Session(engine)

#___________________________________________________________

#FLASK SETUP - CREATE APP
app = Flask(__name__)

#CREATE ROUTES
#List all routes that are available
@app.route("/")
def home_page():
	return (
		f"Welcome to the Climate App!<br/>"
		f"Available routes:<br/>"
		f"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/stations<br/>"
		f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/<start><br/>"
		f"/api/v1.0/<start>/<end><br/>")

#Precipitation Route
@app.route("/api/v1.0/precipitation")

def precipitation():
	#Query
	recent_date2 = dt.date(2017,8,23) - dt.timedelta(365)
	precipitation = session.query(measurement.date,measurement.prcp).filter(measurement.date >= recent_date2).all()
	#Create dictionary 
	precipitation_dict = {date: prcp for date, prcp in precipitation}
	return jsonify(precipitation_dict)

#Stations Route
@app.route("/api/v1.0/stations")

def stations():
	#Query
	results1 = session.query(station.station).all()
	#Unravel & print
	stations1 = list(np.ravel(results1))
	return jsonify(stations1)

#Tobs Route
@ app.route("/api/v1.0/tobs")

def tobs():
	#Query
	recent_date3 = dt.date(2017,8,23) - dt.timedelta(365)
	results = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= recent_date3).all()
	#Unravel & print
	tobs1 = list(np.ravel(results))
	return jsonify(tobs1)

#Start/End Routes
@ app.route("/api/v1.0/<start>")
@ app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):
	print(start,end)

#Queries 
	if not end:
		start_results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= start).all()
		tobs2 = list(np.ravel(start_results))
		return jsonify(tobs2)
	start_results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
	tobs2 = list(np.ravel(start_results))
	return jsonify(tobs2)
	
if __name__ == '__main__':
	app.run()