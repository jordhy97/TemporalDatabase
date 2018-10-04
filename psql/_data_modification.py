import psycopg2
import psycopg2.extras

from .util import _merge_interval
from datetime import datetime

def insert(self, table_name, values):
    try:
        cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        # Cast string to time
        values['valid_from'] = datetime.strptime(values['valid_from'], '%Y-%m-%d').date()
        values['valid_to'] = datetime.strptime(values['valid_to'], '%Y-%m-%d').date()

        # Get column names
        query = "SELECT * FROM {} LIMIT 1".format(table_name)
        cur.execute(query)
        col_names = [a for a in cur.fetchone().keys() if a not in ['valid_from', 'valid_to']]
        
        # Fetch data with same descriptive attrs
        query = "SELECT * FROM {} WHERE ".format(table_name) \
            + " AND ".join(["{} = \'{}\'".format(c, values[c]) for c in col_names])

        cur.execute(query)
        existing_res = cur.fetchall()

        # Append data to be inserted, then recalculate intervals
        existing_res.append(values)
        existing_res = _merge_interval(existing_res)

        # Delete existing data
        query = "DELETE FROM {} WHERE ".format(table_name) \
            + " AND ".join(["{} = \'{}\'".format(c, values[c]) for c in col_names])

        cur.execute(query)

        # Insert new data
        query = "INSERT INTO {} VALUES ".format(table_name) \
            + ", ".join(["(\'{}\')".format("\', \'".join([str(i) for i in item.values()])) for item in existing_res])
        
        cur.execute(query)
        res = cur.rowcount
        self.conn.commit()
        cur.close()

        return res

    except psycopg2.InterfaceError as ie:
        print(ie.message)
        self.init_conn()

    except psycopg2.InternalError as ine:
        print(ine)
        self.conn.rollback()

def delete(self, table_name, values):
    try:
        cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        # Cast string to time
        values['valid_from'] = datetime.strptime(values['valid_from'], '%Y-%m-%d').date()
        values['valid_to'] = datetime.strptime(values['valid_to'], '%Y-%m-%d').date()

        # Get column names
        query = "SELECT * FROM {} LIMIT 1".format(table_name)
        cur.execute(query)
        col_names = [a for a in cur.fetchone().keys() if a not in ['valid_from', 'valid_to']]
        
        # Fetch data with same descriptive attrs
        query = "SELECT * FROM {} WHERE ".format(table_name) \
            + " AND ".join(["{} = \'{}\'".format(c, values[c]) for c in col_names])

        cur.execute(query)
        existing_res = cur.fetchall()

        # Append data to be inserted, then recalculate intervals
        existing_res.append(values)
        existing_res = _merge_interval(existing_res, op='subtract')

        # Delete existing data
        query = "DELETE FROM {} WHERE ".format(table_name) \
            + " AND ".join(["{} = \'{}\'".format(c, values[c]) for c in col_names])

        cur.execute(query)
        res = cur.rowcount

        # Insert new data
        if existing_res:
            query = "INSERT INTO {} VALUES ".format(table_name) \
                + ", ".join(["(\'{}\')".format("\', \'".join([str(i) for i in item.values()])) for item in existing_res])
        
            cur.execute(query)
            res = cur.rowcount
            
        self.conn.commit()
        cur.close()

        return res

    except psycopg2.InterfaceError as ie:
        print(ie.message)
        self.init_conn()

    except psycopg2.InternalError as ine:
        print(ine)
        self.conn.rollback()
