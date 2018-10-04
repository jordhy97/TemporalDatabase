from flask import Flask, request
from flask_cors import CORS, cross_origin
from psql import DB
import json
import psycopg2
from allen import Allen, ValidInterval

from allen import Allen
from allen.allen_predicate_generator import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db = DB(filename='database.ini')

def convert_relation(relation, relation_alias = None):
    if relation_alias is not None:
        return '(' + relation + ') AS ' + relation_alias
    else:
        return relation

def get_non_temporal_attributes(relation, relation_alias = None):
    try:
        cur = db.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        col_names = dict()
        query = "SELECT * FROM " + convert_relation(relation, relation_alias) + " LIMIT 0"
        cur.execute(query)
        print(cur)
        col_names = [desc[0] for desc in cur.description if desc[0] not in ['valid_from', 'valid_to']]
        cur.close()

        return col_names

    except psycopg2.InterfaceError as ie:
        print(ie.message)
        self.init_conn()

    except psycopg2.InternalError as ine:
        print(ine)
        self.conn.rollback()

def create_relation_alias(attributes, alias):
    result = []
    for attribute in attributes:
        result.append(alias + '.' + attribute)
    return result

def temporal_projection_condition(attributes, alias1, alias2):
    alias1_attributes = create_relation_alias(attributes, alias1)
    alias2_attributes = create_relation_alias(attributes, alias2)
    result = ''
    for i in range(len(attributes)):
        if i != 0:
            result += ' AND '
        result += alias1_attributes[i] + ' = ' + alias2_attributes[i]
    return result

def join_condition(attributes1, attributes2, alias1, alias2):
    alias1_attributes = create_relation_alias(attributes1, alias1)
    alias2_attributes = create_relation_alias(attributes2, alias2)
    result = ''
    for i in range(len(attributes1)):
        if i != 0:
            result += ' AND '
        result += alias1_attributes[i] + ' = ' + alias2_attributes[i]
    return result

def temporal_selection(relation, predicates = None, relation_alias = None):
    if predicates is not None:
        return 'SELECT * FROM ' + convert_relation(relation, relation_alias) + ' WHERE ' + predicates
    else:
        return 'SELECT * FROM ' + convert_relation(relation, relation_alias)

def temporal_projection(relation, attributes):
    if " " in relation:
        relation = '(' + relation + ')'
    return ('SELECT DISTINCT ' + ', '.join(create_relation_alias(attributes, 'F')) + ', F.valid_from, L.valid_to'
            ' FROM ' + relation + ' AS F, ' + relation + ' AS L'
            ' WHERE F.valid_from < L.valid_to AND ' + temporal_projection_condition(attributes, 'F', 'L') + ' AND'
            ' NOT EXISTS ( SELECT * FROM ' + relation + ' AS M'
            ' WHERE ' + temporal_projection_condition(attributes, 'M', 'F') + ' AND'
            ' F.valid_from < M.valid_from AND M.valid_from <= L.valid_to'
            ' AND NOT EXISTS ( SELECT * FROM ' + relation + ' AS T1'
            ' WHERE ' + temporal_projection_condition(attributes, 'T1', 'F') + ' AND'
            ' T1.valid_from < M.valid_from AND M.valid_from <= T1.valid_to ) )'
            ' AND NOT EXISTS ( SELECT * FROM ' + relation + ' AS T2'
            ' WHERE ' + temporal_projection_condition(attributes, 'T2', 'F') + ' AND'
            ' ( (T2.valid_from < F.valid_from AND F.valid_from <= T2.valid_to)'
            ' OR (T2.valid_from <= L.valid_to AND L.valid_to <  T2.valid_to) ) )')

def temporal_union(relation1, relation2, relation1_alias = None, relation2_alias = None):
    query = temporal_selection(relation1, relation_alias=relation1_alias) + ' UNION ALL ' + temporal_selection(relation2, relation_alias=relation2_alias)
    return temporal_projection(query, get_non_temporal_attributes(query, "temp"))

def temporal_difference(relation1, relation2, relation1_alias = None, relation2_alias = None):
    if " " in relation1:
        relation1 = '(' + relation1 + ')'
    if " " in relation2:
        relation2 = '(' + relation2 + ')'

    relation1_attributes = get_non_temporal_attributes(relation1, relation1_alias)
    relation2_attributes = get_non_temporal_attributes(relation2, relation2_alias)

    query1 = ('SELECT ' + ', '.join(create_relation_alias(relation1_attributes, 'I1')) + ', I1.valid_from, I2.valid_from AS valid_to'
              ' FROM ' + relation1 + ' AS I1, ' + relation2 + ' AS I2'
              ' WHERE ' + join_condition(relation1_attributes, relation2_attributes, 'I1', 'I2') + ' AND'
              ' I1.valid_from < I2.valid_from AND I2.valid_from < I1.valid_to'
              ' AND NOT EXISTS ( SELECT * FROM ' + relation2 + ' AS I3'
              ' WHERE ' + join_condition(relation1_attributes, relation2_attributes, 'I1', 'I3') + ' AND'
              ' I1.valid_from < I3.valid_to AND I3.valid_from < I2.valid_from )')

    query2 = ('SELECT ' + ', '.join(create_relation_alias(relation1_attributes, 'I1')) + ', I2.valid_to AS valid_from, I1.valid_to'
              ' FROM ' + relation1 + ' AS I1, ' + relation2 + ' AS I2'
              ' WHERE ' + join_condition(relation1_attributes, relation2_attributes, 'I1', 'I2') + ' AND'
              ' I1.valid_from < I2.valid_to AND I2.valid_to < I1.valid_to'
              ' AND NOT EXISTS ( SELECT * FROM ' + relation2 + ' AS I3'
              ' WHERE ' + join_condition(relation1_attributes, relation2_attributes, 'I1', 'I3') + ' AND'
              ' I2.valid_to < I3.valid_to AND I3.valid_from < I1.valid_to )')

    query3 = ('SELECT ' + ', '.join(create_relation_alias(relation1_attributes, 'I1')) + ', I2.valid_to AS valid_from, I3.valid_from AS valid_to'
              ' FROM ' + relation1 + ' AS I1, ' + relation2 + ' AS I2, ' + relation2 + ' AS I3'
              ' WHERE ' + join_condition(relation1_attributes, relation2_attributes, 'I1', 'I2') + ' AND'
              ' ' + join_condition(relation1_attributes, relation2_attributes, 'I1', 'I3') + ' AND'
              ' I2.valid_to < I3.valid_from '
              ' AND I1.valid_from < I2.valid_to'
              ' AND I3.valid_from < I1.valid_to'
              ' AND NOT EXISTS ( SELECT * FROM ' + relation2 + ' AS I4'
              ' WHERE ' + join_condition(relation1_attributes, relation2_attributes, 'I1', 'I4') + ' AND'
              ' I2.valid_to < I4.valid_to AND I4.valid_from < I3.valid_from )')

    query4 = ('SELECT ' + ', '.join(relation1_attributes) + ', valid_from, valid_to'
              ' FROM ' + relation1 + ' AS I1'
              ' WHERE NOT EXISTS ( SELECT * FROM ' + relation2 + ' AS I4'
              ' WHERE ' + join_condition(relation1_attributes, relation2_attributes, 'I1', 'I4') + ' AND'
              ' I1.valid_from < I4.valid_to AND I4.valid_from < I1.valid_to )')

    return query1 + ' UNION ' + query2 + ' UNION ' + query3 + ' UNION ' + query4

def temporal_join(relation1, relation2, relation1_alias = None, relation2_alias = None):
    if " " in relation1:
        relation1 = '(' + relation1 + ')'
    if " " in relation2:
        relation2 = '(' + relation2 + ')'

    relation1_attributes = get_non_temporal_attributes(relation1, relation1_alias)
    relation2_attributes = get_non_temporal_attributes(relation2, relation2_alias)

    join_attributes = [attribute for attribute in relation1_attributes if attribute in relation2_attributes]
    relation1_attributes = [attribute for attribute in relation1_attributes if attribute not in join_attributes]
    relation2_attributes = [attribute for attribute in relation2_attributes if attribute not in join_attributes]

    return ('SELECT ' + ', '.join(create_relation_alias(join_attributes, 'S')) + ', ' + ', '.join(relation1_attributes) + ', ' + ', '.join(relation2_attributes) + ','
            ' CASE WHEN S.valid_from > I.valid_from '
            ' THEN S.valid_from ELSE I.valid_from END AS valid_from, '
            ' CASE WHEN S.valid_to > I.valid_to '
            ' THEN I.valid_to ELSE S.valid_to END AS valid_to'
            ' FROM ' + relation1 + ' AS S, ' + relation2 + ' AS I '
            ' WHERE ' + join_condition(join_attributes, join_attributes, 'S', 'I') + ' AND'
            ' (CASE WHEN S.valid_from > I.valid_from'
            ' THEN S.valid_from ELSE I.valid_from END)'
            ' < (CASE WHEN S.valid_to > I.valid_to'
            ' THEN I.valid_to ELSE S.valid_to END)')

def valid_timeslice(relation, valid_time, relation_alias=None):
    non_temporal_attributes = get_non_temporal_attributes(relation, relation_alias)
    return ('SELECT ' + ', '.join(non_temporal_attributes) +  ' FROM ' + convert_relation(relation, relation_alias) + ' WHERE'
            ' valid_from <= \'' + valid_time + '\' AND \'' + valid_time + '\' <= valid_to')

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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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

@app.route('/insert', methods=['POST'])
@cross_origin()
def insert():
    data = request.get_json(silent=True)

    inserted_data = data['data']
    table = data['table']

    res = db.insert(table, inserted_data)
    return json.dumps(res)

@app.route('/delete', methods=['POST'])
@cross_origin()
def delete():
    data = request.get_json(silent=True)

    deleted_data = data['data']
    table = data['table']

    res = db.delete(table, deleted_data)
    return json.dumps(res)

@app.route('/update', methods=['POST'])
@cross_origin()
def update():
    data = request.get_json(silent=True)

    table = data['table']
    updated_values = data['values']
    update_condition = data['condition']

    res = db.update(table, updated_values, update_condition)
    return json.dumps(res)

@app.route('/query', methods=['POST'])
@cross_origin()
def query():
    data = request.get_json(silent=True)

    query = data['query']
    try:
        cur = db.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(eval(query))
        res = cur.fetchall()
        cur.close()

        if res is not None:
            for r in res:
                if 'valid_from' in r:
                    r['valid_from'] = str(r['valid_from'])
                if 'valid_to' in r:
                    r['valid_to'] = str(r['valid_to'])

        return json.dumps(res)

    except psycopg2.InterfaceError as ie:
        print(ie.message)
        db.init_conn()
        return '{}'

    except psycopg2.InternalError as ine:
        print(ine)
        db.conn.rollback()
        return '{}'

    except:
        return '{}'

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()
