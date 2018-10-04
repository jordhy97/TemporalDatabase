import psycopg2
import psycopg2.extras

from .util import _merge_interval

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

        query = "SELECT * FROM {} WHERE ".format(table_name) \
                + " AND ".join(["{}.{} {} \'{}\'".format(table_name, v['col'], v['op'], v['val'])
                                for v in query_clause])

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
        query = " UNION ".join(["SELECT * FROM {}".format(t) for t in table_names])

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
        query = "SELECT * FROM {}".format(table_names[0]) \
                + "".join([" UNION SELECT * FROM {} WHERE {}".format(
                        t,
                        " AND ".join(["{} IN (SELECT {} FROM {})".format(
                            c,
                            cdiff,
                            table_names[0]
                        ) for i, (c, cdiff) in enumerate(zip(col_names[t], col_names[table_names[0]]))
                    ])) for t in table_names[1:]
                ])

        cur.execute(query)
        res = cur.fetchall()

        cur.close()

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
        query = " UNION ".join([
            "SELECT {} FROM {}{}".format(
                ", ".join([c for c in result_col_names]),
                base_table,
                "".join([" NATURAL JOIN (SELECT {} FROM {}) AS {}_subquery".format(
                    ", ".join([c for c in col_names[t]]),
                    t,
                    t
                ) for t in table_names if t != base_table
            ])) for base_table in table_names
        ])
        
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

def timeslice(self, table_name, time):
    try:
        cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        # Fetch data from DB
        query = """
            SELECT *
            FROM {}
            WHERE valid_from <= \'{}\'::date
                AND valid_to >= \'{}\'::date
        """.format(table_name, time, time)

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
