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

        return res

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
        query_res = cur.fetchall()
        cur.close()

        # Merge intervals
        res_interval_dict = dict()
        for v in query_res:
            try:
                res_interval_dict[v[col_name]] |= I.closed(v['valid_from'], v['valid_to'])
            except KeyError:
                res_interval_dict[v[col_name]] = I.closed(v['valid_from'], v['valid_to'])

        # Convert back to list of dict
        res = list()
        for k, v in res_interval_dict.items():
            for i in v:
                res.append({
                    col_name: k,
                    'valid_from': i.lower,
                    'valid_to': i.upper
                })

        return res

    except psycopg2.InterfaceError as ie:
        print(ie.message)
        self.init_conn()

    except psycopg2.InternalError as ine:
        print(ine)
        self.conn.rollback()