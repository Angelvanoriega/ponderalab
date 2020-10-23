import flask
from db import execute_insert, execute_select, execute_query
app = flask.Flask(__name__)
app.config["DEBUG"] = True
import json
from flask_cors import CORS


CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/getPotTotByCP/<cp>', methods=['GET'])
def getPotTotByCP(cp):
    query = 'select i.cp, sum(pobtot)::text pobtot, sum(pobmas)::text pobmas, sum(pobfem)::text pobfem from ageb a ' \
            ' inner join iter i on i.mun = a.mun and i.loc = a.loc and i.entidad = a.entidad ' \
            ' where i.cp = \'%s\' group by i.cp order by 1 ' % (cp)
    results = execute_select(query)
    return json.dumps(results)

@app.route('/getAllAviableCP', methods=['GET'])
def getAllAviableCP():
    query = 'select i.cp, a.nom_ent from ageb a ' \
            ' inner join iter i on i.mun = a.mun and i.loc = a.loc and i.entidad = a.entidad ' \
            ' where cp != \'\' group by i.cp, a.nom_ent order by 1 '
    results = execute_select(query)
    return json.dumps(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)