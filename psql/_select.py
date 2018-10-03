import psycopg2
import psycopg2.extras

def select_one_table(self, table_name):
    try:
        cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute("""SELECT * FROM {}""".format(table_name))
        return cur.fetchall()
        
    except psycopg2.InterfaceError as ie:
        print(ie.message)
        self.init_conn()