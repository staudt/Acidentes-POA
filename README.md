# Acidentes-POA
Visualização de métricas de acidentes de trânsito em Porto Alegre

Requirements:
> Python (download & install: https://www.python.org/downloads/)
> Flask (download & install: http://flask.pocoo.org/docs/0.10/installation/)

Setup:
1. Unzip the files Acidentes-POA-master/dados/dados.zip into Acidentes-POA-master/dados
2. Run: python rebuild_database.py
3. Run: python run.py 

Endpoints (all based on http://localhost:5000):
> / : main view
> /query/top/<int:n> : get the total top <n> vias with accidents
> /query/top/<campo>/<int:n> : get the <campo> top <n> vias with accidents
> /db/<int:index> : get the json from the row where ID = <index> 
