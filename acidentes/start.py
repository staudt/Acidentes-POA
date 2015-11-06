# -*- coding: utf-8 -*-
# pep8: disable-msg=E501
# pylint: disable=C0301

from acidentes import __version__, log
from flask import render_template
from flask import Flask
import sqlite3
import json


app = Flask(__name__)

def rows_to_dict(rows):
    return [dict((rows.description[i][0], value) \
               for i, value in enumerate(row)) for row in rows.fetchall()]

@app.route("/query/top/<int:count>")
def top(count):
    cur = sqlite3.connect('dados.db')
    query_top_vias = "SELECT COUNT(via) AS ranking, via, latlong FROM acidentes WHERE ano=2014 AND moto=1 GROUP BY via ORDER BY ranking DESC LIMIT %s" % count
    top_vias = rows_to_dict(cur.execute(query_top_vias))
    
    where_vias_para_coordenadas = ' or '.join([("via='%s'" % v['via']) for v in top_vias])
    query_coordenadas = "SELECT latlong FROM acidentes WHERE ano=2014 AND moto=1 AND (%s) LIMIT 3000" % where_vias_para_coordenadas
    coordenadas = [value[-1] for value in cur.execute(query_coordenadas).fetchall()]
    cur.close()
    return json.dumps({'top':top_vias, 'coordinates':coordenadas})
    
@app.route("/")
def tabela():
    return render_template('mapa.html')

def main():
    log.info("Acidentes-POA v" + __version__)
    app.run(host='0.0.0.0', debug=True)
