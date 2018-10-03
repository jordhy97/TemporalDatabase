import psycopg2
import psycopg2.extras
import intervals as I

def select_one_table(self, table_name):
    try:
        cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute("""SELECT * FROM {}""".format(table_name))

        res = cur.fetchall()
        cur.close()
        return res

    except psycopg2.InterfaceError as ie:
        print(ie.message)
        self.init_conn()

    except psycopg2.InternalError as ine:
        print(ine)
        self.conn.rollback()

def select(self, table_name, query_clause):
    try:
        cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        query = "SELECT * FROM {}".format(table_name)
        for i, v in enumerate(query_clause):
            if i == 0:
                query += " WHERE {}.{} {} \'{}\'".format(table_name, v['col'], v['op'], v['val'])
            else:
                query += " AND {}.{} {} \'{}\'".format(table_name, v['col'], v['op'], v['val'])

        cur.execute(query)
        res = cur.fetchall()
        cur.close()

        return _merge_interval(res)

    except psycopg2.InterfaceError as ife:
        print(ife.message)
        self.init_conn()

    except psycopg2.InternalError as ine:
        print(ine)
        self.conn.rollback()

def project(self, table_name, col_name):
    try:
        cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        # Fetch data from DB
        query = "SELECT {}, valid_from, valid_to FROM {}".format(col_name, table_name)

        cur.execute(query)
        res = cur.fetchall()
        cur.close()

        return _merge_interval(res)

    except psycopg2.InterfaceError as ie:
        print(ie.message)
        self.init_conn()

    except psycopg2.InternalError as ine:
        print(ine)
        self.conn.rollback()

def union(self, table_names):
    try:
        cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        # Fetch data from DB
        query = ""
        for i, t in enumerate(table_names):
            if i > 0:
                query += " UNION "
            query += "SELECT * FROM {}".format(t)

        cur.execute(query)
        res = cur.fetchall()
        cur.close()

        return _merge_interval(res)

    except psycopg2.InterfaceError as ie:
        print(ie.message)
        self.init_conn()

    except psycopg2.InternalError as ine:
        print(ine)
        self.conn.rollback()

def set_difference(self, table_names):
    try:
        cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        # Get column names
        col_names = dict()
        for t in table_names:
            query = "SELECT * FROM {} LIMIT 1".format(t)
            cur.execute(query)
            col_names[t] = [a for a in cur.fetchone().keys() if a not in ['valid_from', 'valid_to']]

        # Get base query data
        query = "SELECT * FROM {}".format(table_names[0])

        # Get subtracted data
        for t in table_names:
            if t == table_names[0]:
                continue
            else:
                query += " UNION "
            
            query += "SELECT * FROM {} WHERE ".format(t)
            for i, (c, cdiff) in enumerate(zip(col_names[t], col_names[table_names[0]])):
                if i > 0:
                    query += " AND "
                query += "{} IN (SELECT {} FROM {})".format(c, cdiff, table_names[0])

        cur.execute(query)
        res = cur.fetchall()

        cur.close()
        print(res)

        return _merge_interval(res, op='subtract')

    except psycopg2.InterfaceError as ie:
        print(ie.message)
        self.init_conn()

    except psycopg2.InternalError as ine:
        print(ine)
        self.conn.rollback()

def join(self, table_names):
    try:
        cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        # Get column names
        col_names = dict()
        for t in table_names:
            query = "SELECT * FROM {} LIMIT 1".format(t)
            cur.execute(query)
            col_names[t] = [a for a in cur.fetchone().keys() if a not in ['valid_from', 'valid_to']]
        
        result_col_names = list(set().union(*col_names.values()))
        result_col_names.extend(['valid_from', 'valid_to'])

        # Fetch data from DB
        query = ""
        for i, base_table in enumerate(table_names):
            if i > 0:
                query += " UNION "

            query += "SELECT "
            for j, c in enumerate(result_col_names):
                if j > 0:
                    query += ", "
                query += c
            query += " FROM {}".format(base_table)

            for t in table_names:
                if t != base_table:
                    query += " NATURAL JOIN (SELECT "
                    for j, c in enumerate(col_names[t]):
                        if j > 0:
                            query += ", "
                        query += c
                    query += " FROM {}) AS {}_subquery".format(t, t)
        
        cur.execute(query)
        res = cur.fetchall()
        cur.close()

        return _merge_interval(res, op='intersection')

    except psycopg2.InterfaceError as ie:
        print(ie.message)
        self.init_conn()

    except psycopg2.InternalError as ine:
        print(ine)
        self.conn.rollback()

def _merge_interval(result_set, op='union'):
    if len(result_set) == 0:
        return result_set

    attrs = [a for a in result_set[0].keys() if a not in ['valid_from', 'valid_to']]

    # Merge intervals
    res_interval_dict = dict()
    for v in result_set:
        k = []
        for a in attrs:
            k.append(v[a])
        k = tuple(k)

        try:
            if op == 'subtract':
                res_interval_dict[k] -= I.closed(v['valid_from'], v['valid_to'])
            elif op == 'intersection':
                res_interval_dict[k] &= I.closed(v['valid_from'], v['valid_to'])
            else: # op == 'union'
                res_interval_dict[k] |= I.closed(v['valid_from'], v['valid_to'])
        except KeyError:
            res_interval_dict[k] = I.closed(v['valid_from'], v['valid_to'])

    # Convert back to list of dict
    res = list()
    for k, v in res_interval_dict.items():
        for i in v:
            item = dict()
            for attr, val in zip(attrs, list(k)):
                item[attr] = val

            item['valid_from'] = i.lower
            item['valid_to'] = i.upper

            res.append(item)

    return res
