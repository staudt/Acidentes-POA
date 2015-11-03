#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os
import sys


if __name__ == "__main__":
    tem_arquivos_csv = False
    for filename in os.listdir('%s/dados' % os.getcwd()):
        if filename.endswith('.csv'):
            tem_arquivos_csv = True
            break
    if not tem_arquivos_csv:
        print('ANTES DE EXECUTAR: descompacte o arquivo ./dados/dados.zip no diretorio ./dados')
        print('Sem arquivos em dados/*.csv o banco não pode ser populado')
        sys.exit(1)
    try:
        os.remove('dados.db')
    except:
        print('Nao foi possivel deletar dados.db. Certifique-se que nao esta em uso ou que o arquivo exista')
    con = sqlite3.connect('dados.db')
    con.text_factory = str
    c = con.cursor()
    c.execute('DROP TABLE IF EXISTS ACIDENTES')
    c.execute('CREATE TABLE ACIDENTES (ID,LOCAL_VIA,LOG1,LOG2,PREDIAL1,LOCAL,TIPO_ACID,QUEDA_ARR,DATA_HORA,DATA,DIA_SEM,HORA,FERIDOS,FERIDOS_GR,MORTES,MORTE_POST,FATAIS,AUTO,TAXI,LOTACAO,ONIBUS_URB,ONIBUS_MET,ONIBUS_INT,CAMINHAO,MOTO,CARROCA,BICICLETA,OUTRO,TEMPO,NOITE_DIA,FONTE,BOLETIM,REGIAO,DIA,MES,ANO,FX_HORA,CONT_ACID,CONT_VIT,UPS,CONSORCIO,CORREDOR,LONGITUDE,LATITUDE,custom_via)')
    con.commit()

    for filename in os.listdir('%s/dados' % os.getcwd()):
        if filename.endswith('.csv'):
            with open('%s/dados/%s' % (os.getcwd(), filename), 'r') as f:
                content = f.read()
                first_line_of_file = True
                headers = ''
                data = []
                for row in content.splitlines():
                    if first_line_of_file:
                        headers = str(row).split(';')
                        first_line_of_file = False
                    else:
                        row_data = row.split(';')
                        if len(row_data) == len(headers):
                            row_data = [x.replace(",",".") for x in row_data]
                            if row_data[-1].startswith('-299'): # correcao de um erro no csv original
                                row_data[-1] = row_data[-1].replace('-299', '-29.9')
                            data.append(row_data)
                sql = 'INSERT INTO ACIDENTES (%s) VALUES (%s)' % (','.join(headers), ",".join(['?']*len(headers)))
                c.executemany(sql, data)
                con.commit()
    c.execute("update acidentes set custom_via = local_via where local_via like '%&%'")
    c.execute('''update acidentes set custom_via = log1
                where
                    local_via like '%0%' or
                    local_via like '%1%' or
                    local_via like '%2%' or
                    local_via like '%3%' or
                    local_via like '%4%' or
                    local_via like '%5%' or
                    local_via like '%6%' or
                    local_via like '%7%' or
                    local_via like '%8%' or
                    local_via like '%9%' ''')
    con.commit()
    c.execute('DROP TABLE IF EXISTS ACIDENTES_COUNT')
    c.execute('''
        create table ACIDENTES_COUNT(
                custom_via constraint pk_acidentes_count_custom_via primary key,
                total INTEGER,
                latitude, 
                longitude,
                feridos INTEGER,
                mortes INTEGER,
                fatais INTEGER,
                taxi INTEGER,
                moto INTEGER,
                lotacao INTEGER,
                onibus INTEGER,
                caminhao INTEGER,
                bicicleta INTEGER)''')
    con.commit()
    c.execute('''
        insert into ACIDENTES_COUNT select
                custom_via,
                count(*) as total,
                latitude, longitude,
                SUM(feridos) as feridos,
                SUM(mortes) as mortes,
                SUM(fatais) as fatais,
                SUM(taxi) as taxi,
                SUM(moto) as moto,
                SUM(lotacao) as lotacao,
                SUM(onibus_urb) as onibus,
                SUM(caminhao) as caminhao,
                SUM(bicicleta) as bicicleta
            from acidentes group by custom_via''')
    for i in ["feridos", "mortes", "fatais", "taxi", "moto", "lotacao", "onibus_urb", "caminhao","bicicleta"]:
        c.execute('''create table ACIDENTES_{0} (
                     custom_via constraint pk_acidentes_{0}_custom_via primary key, 
                     ranking INTEGER,
                     points TEXT,
                     FOREIGN KEY (custom_via) references ACIDENTES_COUNT(custom_via)
                     )'''.format(i))
        con.commit()
        c.execute('''
            insert into ACIDENTES_{0} 
                    select custom_via, ranking, points from (select custom_via,
                    SUM({0}) as ranking,
                    group_concat(latitude || ';' || longitude) as points
            from acidentes group by custom_via) where ranking > 0'''.format(i))
        con.commit()
