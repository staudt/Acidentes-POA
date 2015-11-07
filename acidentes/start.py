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
    query = ['ano=' + request.args.get('ano') if request.args.get('ano') else '2014']
    if request.args.get('tipo_acid'): query.append("tipo_acid='%s'" % request.args.get('tipo_acid'))
    if request.args.get('mes'): query.append("mes='%s'" % request.args.get('mes'))
    if request.args.get('dia_sem'): query.append("dia_sem='%s'" % request.args.get('dia_sem'))
    if request.args.get('auto'): query.append("auto=1")
    if request.args.get('moto'): query.append("moto=1")
    if request.args.get('taxi'): query.append("taxi=1")
    if request.args.get('lotacao'): query.append("lotacao=1")
    if request.args.get('onibus'): query.append("onibus=1")
    if request.args.get('caminhao'): query.append("caminhao=1")
    if request.args.get('bicicleta'): query.append("bicicleta=1")
    ranking = 'COUNT(via)' if not request.args.get('ranking') else 'SUM(%s)' % request.args.get('ranking')

    where = ' AND '.join(query)
    query_top_vias = "SELECT %s AS ranking, via, latlng FROM acidentes WHERE %s GROUP BY via HAVING ranking>0 ORDER BY ranking DESC LIMIT %s" % (ranking, where, count)

    cur = sqlite3.connect('dados.db')
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
