from flask import Flask, request
from flask_cors import CORS, cross_origin 
from psql import DB
import json
from allen import Allen, ValidInterval

from allen import Allen

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db = DB(filename='database.ini')

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/table', methods=['GET'])
@cross_origin()
def select_table():
    table_name = request.values['table']

    res = list(db.select_one_table(table_name))
    for r in res:
        r['valid_from'] = str(r['valid_from'])
        r['valid_to'] = str(r['valid_to'])

    return json.dumps(res)

@app.route('/allen', methods=['POST'])
@cross_origin()
def compare_allen():
    data = request.get_json(silent=True)

    i0 = ValidInterval(data['data'][0]['valid_from'], data['data'][0]['valid_to'])
    i1 = ValidInterval(data['data'][1]['valid_from'], data['data'][1]['valid_to'])

    return str(Allen[data['op']](i0, i1))

@app.route('/select', methods=['POST'])
@cross_origin()
def select():
    data = request.get_json(silent=True)

    table_name = data['table']
    query_clause = data['data']

    res = db.select(table_name, query_clause)
    if res is not None:
        for r in res:
            r['valid_from'] = str(r['valid_from'])
            r['valid_to'] = str(r['valid_to'])

    return json.dumps(res)

@app.route('/project', methods=['POST'])
@cross_origin()
def project():
    data = request.get_json(silent=True)

    table_name = data['table']
    col_name = data['col']

    res = db.project(table_name, col_name)
    if res is not None:
        for r in res:
            r['valid_from'] = str(r['valid_from'])
            r['valid_to'] = str(r['valid_to'])

    return json.dumps(res)

@app.route('/union', methods=['POST'])
@cross_origin()
def union():
    data = request.get_json(silent=True)

    table_names = data['tables']

    res = db.union(table_names)
    if res is not None:
        for r in res:
            r['valid_from'] = str(r['valid_from'])
            r['valid_to'] = str(r['valid_to'])

    return json.dumps(res)

@app.route('/set_difference', methods=['POST'])
def set_difference():
    data = request.get_json(silent=True)

    table_names = data['tables']

    res = db.set_difference(table_names)
    if res is not None:
        for r in res:
            r['valid_from'] = str(r['valid_from'])
            r['valid_to'] = str(r['valid_to'])

    return json.dumps(res)

@app.route('/join', methods=['POST'])
def join():
    data = request.get_json(silent=True)

    table_names = data['tables']

    res = db.join(table_names)
    if res is not None:
        for r in res:
            r['valid_from'] = str(r['valid_from'])
            r['valid_to'] = str(r['valid_to'])

    return json.dumps(res)

@app.route('/timeslice', methods=['POST'])
def timeslice():
    data = request.get_json(silent=True)

    table_name = data['table']
    time = data['time']

    res = db.timeslice(table_name, time)
    if res is not None:
        for r in res:
            r.pop('valid_from')
            r.pop('valid_to')

    return json.dumps(res)

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()