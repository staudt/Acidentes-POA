# -*- coding: utf-8 -*-
# pep8: disable-msg=E501
# pylint: disable=C0301

from acidentes import __version__, log
from flask import render_template
from flask import Flask
import sqlite3
import json

app = Flask(__name__)

#http://stackoverflow.com/questions/3286525/return-sql-table-as-json-in-python
def get_data(query, index=-1):
    cur = sqlite3.connect('dados.db')
    d = cur.execute(query)
    r = [dict((d.description[i][0], value) \
               for i, value in enumerate(row)) for row in d.fetchall()]
    cur.close()
    return (r[index] if r else None) if index >= 0 else r
    
@app.route("/db")
def db():
    return json.dumps(get_data("select * from ACIDENTES where LOG1='AV IPIRANGA'"))

@app.route("/db/<int:index>")
def db_index(index):
    return json.dumps(get_data("select * from ACIDENTES where LOG1='AV IPIRANGA'", index))
    
@app.route("/")
def index():
    databaseData = get_data("select * from ACIDENTES where LOG1='AV IPIRANGA'", 0)
    html = render_template('map.html', data = json.dumps(databaseData))
    return html

def main():
    log.info("Acidentes-POA v" + __version__)
    app.run(host='0.0.0.0', debug=True)
