#!/usr/bin/env python

from flask import Flask
from pymongo import MongoClient
import os
import time

app = Flask(__name__)

# Debug switches for RH openshift
DEBUG='true'
app.config['PROPAGATE_EXCEPTIONS'] = True

os.environ['TZ'] = 'Europe/London'
time.tzset()
   
""" Mongo DB string, this will soon contain parameters from the 
config-secure.yml configuration file
"""
mongoDBString = ('mongodb://username:password' + os.environ['OPENSHIFT_MONGODB_DB_HOST'] + ':' + os.environ['OPENSHIFT_MONGODB_DB_PORT'] + '/')

""" Location functions

These functions are used to take the location values submitted as part of the 
get request and use them as a update variable for the database. 

The retrieval function in the core nead application [which sites on the pi]
uses a very simple if else to parse the database faux locations and return the
 real values we want to use. 

"""

@app.route('/location/<location>')
def location(location):

    # Some nasty nasty input vertification
    if (location == "location1"):  
        updateDBLocation('location1')
    elif (location == "location2"):
        updateDBLocation('location2')
    elif (location == "location3"):
        updateDBLocation('location3')
  
    string = ("complete")

    return string

def updateDBLocation(locationDetail):

    client = MongoClient(mongoDBString)
 
    # For local mongo testing
    # client = MongoClient()
 
    db = client.dashdb

    queryResult = db.nead.update (
        { "widget": "location" },
        { "$set":
            { "location": locationDetail }
        },
        upsert=False, multi=False
    )

@app.route('/location/display')
def displayLocation():

    client = MongoClient(mongoDBString)

    # For local mongo testing
    # client = MongoClient()

    db = client.dashdb

    cursor = db.nead.find()

    for object in cursor: 
        data = object['location']

    return data

""" Coffee functions

Push the current date and time of the request for /coffee/plus to the mongo database

"""
@app.route('/coffee/plus')
def updateCoffeeCount():

    currentDate = time.strftime("%Y-%m-%d")
    currentTime = time.strftime("%H:%M")

    client = MongoClient(mongoDBString)

    # For local mongo testing
    # client = MongoClient()

    db = client.dashdb

    result = db.coffee.insert({"currentDate": currentDate, "currentTime": currentTime})

    return "complete"


@app.route('/coffee/status')
def showCoffeeCount():

    currentDate = time.strftime("%Y-%m-%d")

    count = 0

    client = MongoClient(mongoDBString)

    db = client.dashdb

    cursor = db.coffee.find({'currentDate': currentDate })

    for object in cursor: 
        data = object['currentDate']
        count = count + 1

    return str(count)

if __name__ == '__main__':
    app.run(port=8051,debug="True")
