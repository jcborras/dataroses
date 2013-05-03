#!/usr/bin/env python
# -*- coding: utf-8

__author__ = 'jcb'

from csv import DictReader
from datetime import datetime
from json import dumps
from logging import basicConfig, DEBUG
from random import sample
from string import ascii_letters, digits
from StringIO import StringIO

from colorbrewer import html_form, qualitative
from flask import Flask, render_template, url_for, escape, session
from flask import request, redirect
from pymongo import Connection, MongoClient

APP_PORT = 5000
APP_HOSTNAME = 'localhost'
MONGO_DBNAME = 'dataroses'
COLLECTION_NAME = 'roses'

ROOT_URL='/'
CATCHER_URL = ROOT_URL
GRAPH_URL = ROOT_URL + 'graph/'

app = Flask('DataRoses')
formatstr = "%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s"
basicConfig(format=formatstr, level=DEBUG)
app.logger.setLevel(DEBUG)

def get_collection(logger=app.logger):
    logger.debug('Looking for database')
    conn, cli = Connection(), MongoClient()
    if MONGO_DBNAME not in cli.database_names():
        app.logger.debug('Database missing. Will create one')
        db = conn[MONGO_DBNAME]
        db.create_collection(COLLECTION_NAME)
        return db[COLLECTION_NAME]
    app.logger.debug('Database exists. Returning collection cursor')
    return cli[MONGO_DBNAME][COLLECTION_NAME]

collection = get_collection(app.logger)

## View functions. Their names should match nvd3.js conventions
def BulletChart(x):
    return render_template("TODO")

def SimpleLine(x):
    return render_template('home.html')

def lineChart(x):
    x = DictReader(StringIO(x))
    l = list(x)
    names = x.fieldnames
    cmap = qualitative['Set1'][max(len(names), 3)]
    y = map(lambda n: {'values':[{'x':i, 'y':float(l[i][names[n]])} for i in range(len(l))], 'key':names[n], 'color':html_form(cmap[n])}, range(len(names)))
    app.logger.debug(y)
    return render_template('lineChart.html', data=y)

def Scatter(x):
    return render_template("TODO")

#http://stackoverflow.com/questions/7936572/python-call-a-function-from-string-name
def chart_handler_for(s):
    """Must return a function that renders a canvas graph with the input data"""
    ss = globals().copy()
    ss.update(locals())
    f = ss.get(s)    
    if not f:
        raise Exception("Method %s not implemented" % s)
    return f


SYMBOL_SET = ascii_letters+digits
def random_key():
    return reduce(lambda x,y: x+y, sample(SYMBOL_SET,1))
    
@app.route(ROOT_URL, methods=['GET'])
def frontpage():
    return render_template('home.html')

##http://stackoverflow.com/questions/7936572/python-call-a-function-from-string-name
@app.route(CATCHER_URL + '<chart_type>', methods=['POST'])
def catcher(chart_type):
    h = chart_handler_for(chart_type)
    k = random_key()
    app.logger.debug(request.form.keys()[0])
    d = {'datetime_utc':datetime.now(), 'graph_id':k, 'chart_type':chart_type,
         'data': request.form.keys()[0]}
    collection.insert(d)
    return str("http://%s:%d%s" % (APP_HOSTNAME, APP_PORT, GRAPH_URL) + k + '\n')
    

@app.route(GRAPH_URL + '<graph_key>', methods=['GET'])
def canvas(graph_key):
    d = collection.find_one({'graph_id':graph_key})
    if d is None:
        app.logger.error('%s key not found' % graph_key)
        return 'boo!', 404
    return chart_handler_for(d['chart_type'])(d['data'])

if __name__ == '__main__':
    #app.logger.debug(app.template_folder)
    #app.logger.info(app.static_folder)
    #app.logger.warning(app.static_url_path)
    #app.logger.error(app.root_path)
    #app.logger.fatal(app.secret_key)
    #app.run(host=slc.app_hostname(), port=slc.app_port(), debug=True)
    app.run(host=APP_HOSTNAME, port=APP_PORT, debug=True)
    #app.run(debug=True)
