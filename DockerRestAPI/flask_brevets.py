"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
from flask_restful import Resource, Api, request 
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
from pymongo import MongoClient
import logging
import os

###
# Globals
###
app = flask.Flask(__name__)
api = Api(app)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY
#client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
client = MongoClient(host="db", port=27017)
db = client.brevetdb

class listAll(Resource):
    def get(self):
        args = request.args
        top = False
        try:
            top = args["top"]
        except:
            pass
        if (top!=False):
            if(top.isnumeric()):
                top = int(top)
            else:
                top = False

        _items = db.brevetdb.find()
        items = [item for item in _items]
        open_times = []
        close_times = []
        for item in items:
            open_times.append(item["start_time"])
            close_times.append(item["close_time"])

        if (top!=False):
            open_times = open_times[0:top]
            close_times = close_times[0:top]

        return { 
                "open_times" : open_times, 

                "close_times" : close_times 
                }

class listOpenOnly(Resource):
    def get(self):
        args = request.args
        top = False
        try:
            top = args["top"]
        except:
            pass
        if (top!=False):
            if(top.isnumeric()):
                top = int(top)
            else:
                top = False

        _items = db.brevetdb.find()
        items = [item for item in _items]
        open_times = []

        for item in items:
            open_times.append(item["start_time"])
        
        if (top!=False):
            open_times = open_times[0:top]

        return {"open_times" : open_times}

class listCloseOnly(Resource):
    def get(self):
        args = request.args
        top = False
        try:
            top = args["top"]
        except:
            pass
        if (top!=False):
            if(top.isnumeric()):
                top = int(top)
            else:
                top = False

        _items = db.brevetdb.find()
        items = [item for item in _items]
        close_times = []

        for item in items:
            close_times.append(item["close_time"])

        if (top!=False):
            close_times = close_times[0:top]

        return {"close_times" : close_times}

class allCSV(Resource):
    def get(self):
        args = request.args
        top = False
        try:
            top = args["top"]
        except:
            pass
        if (top!=False):
            if(top.isnumeric()):
                top = int(top)
            else:
                top = False

        _items = db.brevetdb.find()
        items = [item for item in _items]
        open_times = []
        close_times = []
        open_csv = ""
        close_csv = ""
        for item in items:
            open_times.append(item["start_time"])
            close_times.append(item["close_time"])

        if (top != False):
            for i in range(top):
                open_csv = open_csv + open_times[i] + ","
                close_csv = close_csv + close_times[i] + ","
        else: 
            for item in open_times:
                open_csv = open_csv + item + ","

            for item in close_times:
                close_csv = close_csv + item + ","

        return {"open_times" : open_csv, "close_times" : close_csv}

class openCSV(Resource):
    def get(self):
        args = request.args
        top = False
        try:
            top = args["top"]
        except:
            pass
        if (top!=False):
            if(top.isnumeric()):
                top = int(top)
            else:
                top = False
        _items = db.brevetdb.find()
        items = [item for item in _items]
        open_times = []
        open_csv = ""
        for item in items:
            open_times.append(item["start_time"])

        if (top != False):
            for i in range(top):
                open_csv = open_csv + open_times[i] + ","
        else: 
            for item in open_times:
                open_csv = open_csv + item + ","

        return {"open_times" : open_csv}

class closeCSV(Resource):
    def get(self):
        args = request.args
        top = False
        try:
            top = args["top"]
        except:
            pass
        if (top!=False):
            if(top.isnumeric()):
                top = int(top)
            else:
                top = False

        _items = db.brevetdb.find()
        items = [item for item in _items]
        close_times = []
        close_csv = ""
        for item in items:
            close_times.append(item["close_time"])

        if (top != False):
            for i in range(top):
                open_csv = open_csv + open_times[i] + ","
        else: 
            for item in close_times:
                close_csv = close_csv + item + ","

        return {"close_times" : close_csv}

api.add_resource(allCSV, "/listall/csv")
api.add_resource(openCSV, "/listopenonly/csv")
api.add_resource(closeCSV, "/listcloseonly/csv")
api.add_resource(listAll, "/listall", "/listall/json")
api.add_resource(listOpenOnly, "/listopenonly", "/listopenonly/json")
api.add_resource(listCloseOnly, "/listcloseonly", "/listcloseonly/json")

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    start_date = request.args.get("start_date", "", type=str)
    start_time = request.args.get("start_time", "", type=str)
    distance = request.args.get("distance", type=int)
    date_time = start_date + " " + start_time 
    starting_arrow = arrow.get(date_time, "YYYY-MM-DD HH:mm").isoformat()
    #sstarting_arrow = arrow.get(date_time, "YYYY-MM-DD HH:mm")
    #sstarting_arrow = "HH:mm"
    #starting_arrow = arrow.get(date_time, "YYYY-MM-DD HH:mm").isoformat()
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME: These probably aren't the right open and close times
    # and brevets may be longer than 200km
    open_time = acp_times.open_time(km, distance, starting_arrow)
    #open_time = acp_times.open_time(km, 200, arrow.now().isoformat)
    close_time = acp_times.close_time(km, distance, starting_arrow)
    #close_time = acp_times.close_time(km, 200, arrow.now().isoformat)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/_check")
def new():
    _items = db.brevetdb.find()
    result  = {"pop" : False}
    if(_items != {}):
        db.brevetdb.remove()
        result  = {"pop" : True}
    return flask.jsonify(result=result)


@app.route("/_submit_to_database")
def submit_to_database():
    km = request.args.get('km', 999, type=float)
    start_time = request.args.get('start_time', "", type=str)
    close_time = request.args.get('close_time', "", type=str)
    result = {"km": km, "start": start_time, "close": close_time}
    if(start_time == 'Invalid date'):
        return flask.jsonify(result=result)

    item_doc = {
        'km': km,
        'start_time': start_time,
        'close_time': close_time
    }
    db.brevetdb.insert_one(item_doc)

    return flask.jsonify(result=result)

@app.route("/display")
def display():
    _items = db.brevetdb.find()
    items = [item for item in _items]
    #reset databse after we display it 
    db.brevetdb.remove()
    return flask.render_template("database_display.html", items=items)

@app.route("/_display_database")
def display_database():
    result = {"test": True}
    #print("HERE")
    return flask.jsonify(result=result)
    #return flask.render_template('test.html')
    #return flask.render_template('database_display.html', items=items)
    #return flask.render_template('database_display.html')

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
