# -*- coding: utf-8 -*-
# pep8: disable-msg=E501
# pylint: disable=C0301

from acidentes import __version__, log
from flask import request, render_template
from flask import Flask
import sqlite3
import json
import os.path
import sys


app = Flask(__name__)

def rows_to_dict(rows):
    return [dict((rows.description[i][0], value) \
               for i, value in enumerate(row)) for row in rows.fetchall()]

@app.route("/query/top/<int:count>")
def top(count):
    cur = sqlite3.connect('dados.db')

    where = 'ano=%s' % request.args.get('ano')
    query_top_vias = "SELECT COUNT(via) AS ranking, via, latlng FROM acidentes WHERE %s GROUP BY via ORDER BY ranking DESC LIMIT %s" % (where, count)
    top_vias = rows_to_dict(cur.execute(query_top_vias))
    
    vias_para_coordenadas = ", ".join([("'%s'" % v['via']) for v in top_vias])
    query_coordenadas = "SELECT latlng FROM acidentes WHERE %s AND via IN (%s) LIMIT 8000" % (where, vias_para_coordenadas)
    coordenadas = [value[-1] for value in cur.execute(query_coordenadas).fetchall()]

    cur.close()

    return json.dumps({'top': top_vias, 'coordenadas': coordenadas})
    
@app.route("/")
def tabela():
    return render_template('mapa.html')

def main():
    if not os.path.exists('dados.db'):
        print('ERRO: Banco de dados (dados.db) nao encontrado!')
        print('      execute rebuild_database.py antes de rodar o servidor')
        sys.exit(1)
    log.info("Acidentes-POA v" + __version__)
    app.run(host='0.0.0.0', debug=True)
