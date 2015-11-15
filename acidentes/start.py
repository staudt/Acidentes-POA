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

DATABASE = 'dados.db'

def rows_to_dict(rows):
    return [dict((rows.description[i][0], value) \
               for i, value in enumerate(row)) for row in rows.fetchall()]

def get_where(request_args, ano, via = None):
    query = ['ano=' + ano]
    if request_args.get('tipo_acid'): query.append("tipo_acid='%s'" % request_args.get('tipo_acid'))
    if request_args.get('mes'): query.append("mes='%s'" % request_args.get('mes'))
    if request_args.get('dia_sem'): query.append("dia_sem='%s'" % request_args.get('dia_sem'))
    if request_args.get('auto'): query.append("auto>0")
    if request_args.get('moto'): query.append("moto>0")
    if request_args.get('taxi'): query.append("taxi>0")
    if request_args.get('lotacao'): query.append("lotacao>0")
    if request_args.get('onibus'): query.append("onibus>0")
    if request_args.get('caminhao'): query.append("caminhao>0")
    if request_args.get('bicicleta'): query.append("bicicleta>0")
    if via: query.append("via='"+via+"'")
    where = ' AND '.join(query)
    return where

def get_top_vias(request_args, cur, where, count):
    ranking = 'COUNT(via)' if not request_args.get('ranking') else 'SUM(%s)' % request_args.get('ranking')    
    query_top_vias = "SELECT %s AS ranking, via, latlng FROM acidentes WHERE %s GROUP BY via HAVING ranking>0 ORDER BY ranking DESC LIMIT %s" % (ranking, where, count)
    top_vias = rows_to_dict(cur.execute(query_top_vias))
    return top_vias
    
@app.route("/query/via/<via>")
def via(via):
    """Retorna a contagem de acidentes de 2000 a 2014"""
    cur = sqlite3.connect(DATABASE)
    anos = ','.join(["2000", "2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014"])
    data = [value[-1] for value in cur.execute("SELECT ano, COUNT(ano) AS contagem FROM acidentes WHERE ano IN(%s) and via='%s' GROUP BY ano" % (anos, via)).fetchall()]
    cur.close()
    return json.dumps(data)
    
@app.route("/query/top/<int:count>")
def top(count):
    cur = sqlite3.connect(DATABASE)
    ano = request.args.get('ano') if request.args.get('ano') else '2014'
    where = get_where(request.args, ano)
    
    top_vias = get_top_vias(request.args, cur, where, count)
    
    vias_para_coordenadas = ", ".join([("'%s'" % v['via']) for v in top_vias])
    query_coordenadas = "SELECT latlng || ';' || via FROM acidentes WHERE %s AND via IN (%s)" % (where, vias_para_coordenadas)
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
