import psycopg2
from configparser import ConfigParser

# http://www.postgresqltutorial.com/postgresql-python/connect/

class DB:
    def __init__(self, filename='database.ini'):
        self.params = config(filename)
        self.conn = None
        self.init_conn()

    def init_conn(self):
        try:
            self.conn = psycopg2.connect(**self.params)
        except psycopg2.DatabaseError as de:
            raise

    def test(self):
        cur = self.conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
 
        db_version = cur.fetchone()
        print(db_version)

    from ._temporal_algebra import select_one_table, select, project, union, set_difference, join, timeslice
    from ._data_modification import insert, delete, update


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    
    return db
 
if __name__ == '__main__':
    DB('../database.ini').test()
        