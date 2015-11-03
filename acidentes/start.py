# -*- coding: utf-8 -*-
# pep8: disable-msg=E501
# pylint: disable=C0301

from acidentes import __version__, log
from flask import render_template
from flask import Flask
import sqlite3
import json

TOP_N_OLD = """
select via, round({0}*1.0/custom_max, 4) as ranking, latitude, longitude from
(select a.custom_via as via,
		a.{0},
		(select max({0}) from ACIDENTES_COUNT) as custom_max,
		a.latitude as latitude, a.longitude as longitude
from ACIDENTES_COUNT a)
order by 2 desc
limit {1}
"""
TOP_N_TOTAL = """select custom_via as via, total as ranking, latitude, longitude
            from ACIDENTES_COUNT order by ranking DESC limit {0}"""

TOP_N = """ select custom_via as via, ranking, points
            from ACIDENTES_{0} order by ranking DESC limit {1}"""
            
app = Flask(__name__)

#http://stackoverflow.com/questions/3286525/return-sql-table-as-json-in-python
def get_data(query, index=-1):
    cur = sqlite3.connect('dados.db')
    d = cur.execute(query)
    r = [dict((d.description[i][0], value) \
               for i, value in enumerate(row)) for row in d.fetchall()]
    cur.close()
    return (r[index] if r else None) if index >= 0 else r

@app.route("/query/top/<int:n>")
def top(n):
    return json.dumps(get_data(TOP_N.format('total', str(n))))
    
@app.route("/query/top/<campo>/<int:n>")
def top_campo(campo, n):
    return json.dumps(get_data(TOP_N.format(campo, str(n))))

@app.route("/db/<int:index>")
def db_index(index):
    return json.dumps(get_data("select * from ACIDENTES where ID = '" + index + "'", 0))

@app.route("/")
def tabela():
    return render_template('mapa.html')

def main():
    log.info("Acidentes-POA v" + __version__)
    app.run(host='0.0.0.0', debug=True)
