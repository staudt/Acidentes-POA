#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os
import zlib


if __name__ == "__main__":
    con = sqlite3.connect('dados.db')
    con.text_factory = str
    c = con.cursor()
    c.execute('DROP TABLE IF EXISTS ACIDENTES')
    c.execute('CREATE TABLE ACIDENTES (ID,LOCAL_VIA,LOG1,LOG2,PREDIAL1,LOCAL,TIPO_ACID,QUEDA_ARR,DATA_HORA,DATA,DIA_SEM,HORA,FERIDOS,FERIDOS_GR,MORTES,MORTE_POST,FATAIS,AUTO,TAXI,LOTACAO,ONIBUS_URB,ONIBUS_MET,ONIBUS_INT,CAMINHAO,MOTO,CARROCA,BICICLETA,OUTRO,TEMPO,NOITE_DIA,FONTE,BOLETIM,REGIAO,DIA,MES,ANO,FX_HORA,CONT_ACID,CONT_VIT,UPS,CONSORCIO,CORREDOR,LONGITUDE,LATITUDE)')
    con.commit()

    for filename in os.listdir('%s/dados' % os.getcwd()):
        if filename.endswith('.csv.zlib'):
            with open('%s/dados/%s' % (os.getcwd(), filename), 'rb') as f:
                content = zlib.decompress(f.read())
                first_line_of_file = True
                headers = ''
                data = []
                for row in content.split("\r\n"):
                    if first_line_of_file:
                        headers = row.split(';')
                        
                        first_line_of_file = False
                    else:
                        row_data = row.split(';')
                        if len(row_data) == len(headers):
                            row_data = [x.replace(",",".") for x in row_data]
                            data.append(row_data)
                sql = 'INSERT INTO ACIDENTES (%s) VALUES (%s)' % (','.join(headers), ",".join(['?']*len(headers)))
                c.executemany(sql, data)
                con.commit()

