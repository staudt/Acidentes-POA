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
        sys.exit(1)
    con = sqlite3.connect('dados.db')
    con.text_factory = str
    c = con.cursor()
    c.execute('DROP TABLE IF EXISTS ACIDENTES')
    c.execute('''CREATE TABLE ACIDENTES (
                    VIA text,
                    LOCAL text,     -- Logradouro, cruzamento, etc
                    TIPO_ACID text, -- Abalroamento, Atropelamento, etc
                    DIA_SEM text,    -- Sexta-feira, etc
                    DIA int,
                    MES int,
                    ANO int,
                    LATLONG text,    -- (precessar) latitude;longitude
                -- contagens
                    FERIDOS int,    -- FERIDOS + FERIDOS_GR
                    MORTES int,     -- MORTES + MORTES_POST
                -- booleanos
                    FATAL int,      -- FATAIS
                    AUTO int,       -- automovel
                    TAXI int,
                    LOTACAO int,
                    ONIBUS int,     -- ONIBUS_URB
                    CAMINHAO int,
                    MOTO int,
                    CARROCA int,
                    BICICLETA int,
                    NOITE int       -- 0.dia 1.noite
                );
    ''')
    c.execute('CREATE INDEX VIAINDEX ON ACIDENTES (VIA);');
    c.execute('CREATE INDEX ANOINDEX ON ACIDENTES (ANO);');
    
    for filename in os.listdir('%s/dados' % os.getcwd()):
        if filename.endswith('.csv'):
            print('Processando %s' % filename)
            with open('%s/dados/%s' % (os.getcwd(), filename), 'r') as f:
                content = f.read().splitlines()
                headers = str(content[0]).split(';')
                data = []
                for row_content in content[1:]:
                    row = row_content.split(';')
                    if len(row) == len(headers):
                        row = [x.replace(",",".") for x in row]
                        data.append([
                            row[headers.index('LOG1')].capitalize() + (
                                ' & %s' % row[headers.index('LOG2')].capitalize() if len(row[headers.index('LOG2')])>1 else ''
                            ),
                            row[headers.index('LOCAL')].capitalize(),
                            row[headers.index('TIPO_ACID')].capitalize(),
                            row[headers.index('DIA_SEM')].capitalize(),
                            int(row[headers.index('DIA')]),
                            int(row[headers.index('MES')]),
                            int(row[headers.index('ANO')]),
                            '%s;%s' % (
                                row[headers.index('LATITUDE')].replace('-299', '-29.9'), # fix de um erro nos CSVs
                                row[headers.index('LONGITUDE')]
                            ),
                            
                            int(row[headers.index('FERIDOS')]),
                            int(row[headers.index('MORTES')]),

                            int(row[headers.index('FATAIS')]),
                            int(row[headers.index('AUTO')]),
                            int(row[headers.index('TAXI')]),
                            int(row[headers.index('LOTACAO')]),
                            int(row[headers.index('ONIBUS_URB')]),
                            int(row[headers.index('CAMINHAO')]),
                            int(row[headers.index('MOTO')]),
                            int(row[headers.index('CARROCA')]),
                            int(row[headers.index('BICICLETA')]),
                            1 if row[headers.index('NOITE_DIA')]=='NOITE' else 0,
                        ])

                sql = '''INSERT INTO ACIDENTES VALUES (%s)''' % (",".join(['?']*len(data[0])))
                c.executemany(sql, data)
                con.commit()
    
    print('Pronto!')
