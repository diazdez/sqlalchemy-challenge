import numpy as np
import pandas as pd 
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup (similar to what is found in our "starter" Jupyter Notebook)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# References to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask API Setup
app = Flask(__name__)

# Flask Routes: 

@app.route("/")
def welcome():
     #List all API routes that are available. 
    return (
        f"<h3><br/><h3>"
        f"<h1>Welcome to Hawaii's Climate Analysis' website!<br/><h1>"
        f"<h3><br/><h3>" 
        f"<h3>***The following Routes will provide you with specific data analysis*** <br/><h3>"
        f"<br/>" 
        f"Route for Precipitation data:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>" 
        f"Route for Stations data:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>" 
        f"Route for temperature analysis between 8/23/2016 - 8/23/2017:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>" 
        f"Route for Minimum (TMIN), Maximum (TMAX) and Average (TAVG) temperatures for given 'start date':<br/>" 
        f"(Note: When entering dates, please use 'yyyy-mm-dd' format)<br/>"
        f"  * For example, the following route is for a given 'start date' of Januauy 1, 2016:<br/>"
            f"/api/v1.0/2016-01-01<br/>"
        f"/api/v1.0/&lt;start date&gt;<br/>"
        f"<br/>" 
        f"Route for Minimum (TMIN), Maximum (TMAX) and Average (TAVG) temperatures for a given 'start date' and 'end date':<br/>" 
        f"(Note: When entering dates, please use 'yyyy-mm-dd' format)<br/>"
        f"  * For example, the following route is for a given Start Date of Januauy 1, 2016 and End Date of Januauy 31, 2016:<br/>"
            f"/api/v1.0/2016-01-01/2016-01-31<br/>"
        f"/api/v1.0/&lt;start date&gt;/&lt;end date&gt;<br/>"
        f"<h4><br/><h4>"
        f"<h5>--------                THANK YOU               ---------<h5>"
        f"<h4><br/><h4>"
    )


########################################################################################################################################

@app.route("/api/v1.0/precipitation")
def precipitation(): 

    # create our session (link) from Python to the DB
    session = Session(engine)

    # query for the dates and precipitation values for the last year
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    # Convert the query results to a dictionary using date as the key and prcp as the value. 
    prcp_list = []

    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict ["Date"]  = date
        prcp_dict ["precipitation"]  = prcp
        prcp_list.append(prcp_dict)

    session.close()

    #Return the JSON representation of the dictionary.
    return jsonify(prcp_list)

##########################################################

@app.route("/api/v1.0/stations")
def stations():
    #Create our session (link) from Python to the DB
    session = Session(engine)

    stations_results = session.query(Station.station, Station.name).all()

    #Obtain List of Stations
    stations_list = []
    
    for station, name in stations_results:
        st_dict = {}
        st_dict["station"]= station 
        st_dict["name (location)"] = name 
        stations_list.append(st_dict)
    
    session.close()
 
    return jsonify(stations_list)

##########################################################
@app.route("/api/v1.0/tobs")
def tobs(): 

    # Create a session (link) from Python to the DB
    session = Session(engine)

# last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
# last_year_date = (dt.datetime.strptime(last_date[0],'%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    # The last day in the db is 2017-08-23
    # So, the date 1 year ago from the last day's data point in the database is  2016-08-23


    # Query for the dates and temperature values
    # the date 1 year ago from the last day's data point in the database is 2016-08-23
    tobs_results =   session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date.between('2016-08-23', '2017-08-23')).\
                order_by(Measurement.date).all()

    # Convert to list of dictionaries to jsonify
    tobs_list= []

    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobs_list.append(tobs_dict)

    session.close()

    return jsonify(tobs_list)


##########################################################

@app.route("/api/v1.0/<start>") 
def start(start):
    
# Create a session (link) from Python to the DB
    session = Session(engine)
    

#Return a JSON list of the minimum temperature, the average temperature, \
# and the max temperature for a given start date

    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
 
    results_list= []
    for min,avg,max in results:
        results_dict = {}
        results_dict["TMIN"] = min
        results_dict["TAVG"] = avg
        results_dict["TMAX"] = max 
        results_list.append(results_dict)
    session.close()    

    return jsonify(results)

##########################################################
## Actual START DATE (January 1, 2016)
@app.route("/api/v1.0/2016-01-01") 
def start1(start="2016-01-01"):

# Create a session (link) from Python to the DB
    session = Session(engine)
    

#Return a JSON list of the minimum temperature, the average temperature, \
# and the max temperature for a given start date

    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
 
    results_list= []
    for min,avg,max in results:
        results_dict = {}
        results_dict["TMIN"] = min
        results_dict["TAVG"] = avg
        results_dict["TMAX"] = max 
        results_list.append(results_dict)
    session.close()    

    return jsonify(results_list)


#######################################

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    # Create a session (link) from Python to the DB
    session = Session(engine)

#When given the start only, calculate TMIN, TAVG, and TMAX for all \
# dates greater than and equal to the start date.


    results2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()


    results2_list= []
    for min,avg,max in results2:
        results2_dict = {}
        results2_dict["TMIN"] = min
        results2_dict["TAVG"] = avg
        results2_dict["TMAX"] = max 
        results2_list.append(results2_dict)
    session.close()    

    return jsonify(results2)


###############################

## Start and End DATES provided
@app.route("/api/v1.0/2016-01-01/2016-01-31")
def start_end2(start="2016-01-01", end="2016-01-31"):

    # Create a session (link) from Python to the DB
    session = Session(engine)

#When given the start only, calculate TMIN, TAVG, and TMAX for all \
# dates greater than and equal to the start date.


    results2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()


    results2_list= []
    for min,avg,max in results2:
        results2_dict = {}
        results2_dict["TMIN"] = min
        results2_dict["TAVG"] = avg
        results2_dict["TMAX"] = max 
        results2_list.append(results2_dict)
    session.close()    

    return jsonify(results2_list)


###############################

if __name__ == '__main__':
    app.run(debug=True)
