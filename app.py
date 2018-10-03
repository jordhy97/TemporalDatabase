from flask import Flask, request
from psql import DB
import json
from allen import Allen, ValidInterval

from allen import Allen

app = Flask(__name__)
db = DB(filename='database.ini')

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/select', methods=['GET'])
def select_table():
    table_name = request.values['table']

    res = list(db.select_one_table(table_name))
    for r in res:
        r['valid_from'] = str(r['valid_from'])
        r['valid_to'] = str(r['valid_to'])

    return json.dumps(res)

@app.route('/allen', methods=['POST'])
def compare_allen():
    data = request.get_json(silent=True)

    i0 = ValidInterval(data['data'][0]['valid_from'], data['data'][0]['valid_to'])
    i1 = ValidInterval(data['data'][1]['valid_from'], data['data'][1]['valid_to'])

    return str(Allen[data['op']](i0, i1))

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()