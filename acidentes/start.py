# -*- coding: utf-8 -*-
# pep8: disable-msg=E501
# pylint: disable=C0301

from acidentes import __version__, log
from flask import Flask
import sqlite3

app = Flask(__name__)

def get_database_cursor():
    con = sqlite3.connect('dados.db')
    return con.cursor()

@app.route("/test")
def test():
    c = get_database_cursor()
    c.execute("select * from ACIDENTES where LOG1='AV IPIRANGA'")
    return str(c.fetchone())

@app.route("/")
def index():
    return "Hello World!"

def main():
    log.info("Acidentes-POA v" + __version__)
    app.run(host='0.0.0.0', debug=True)
