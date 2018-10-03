import psycopg2
import psycopg2.extras

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