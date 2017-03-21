# -*- coding: utf-8 -*-

from MySQLdb import cursors

FIELD_NAMES = { 'items': ('item', 'timestamp', 'title', 'price', 'sold_quantity', 'available_quantity', 'seller'),
                'seller': ('seller', 'timestamp', 'nickname', 'city', 'state', 'canceled_transactions', 'completed_transactions', 'reputation')
            }
FIELD_TYPES = { 'items': ('"{1}"', '"{2}"', '"{3}"', '{4}', '{5}', '{6}', '"{7}"'),
                'seller': ('{1}', '"{2}"', '"{3}"', '"{4}"', '"{5}"', '{6}', '{7}', '"{8}"')
            }

def make_query(query, table, fields=None):
    if (query == 'upsert'):
        return 'INSERT INTO {0} (' + ','.join(FIELD_NAMES[table]) + ') VALUES (' + ','.join(FIELD_TYPES[table]) + ') ON DUPLICATE KEY UPDATE end = "{1}"';

    if (query == 'insert'):
        return ('INSERT INTO {0} (' + ','.join(FIELD_NAMES[table]) + ') VALUES (' + ','.join(FIELD_TYPES[table]) + ')');

    if (query == 'select'):
        return 'SELECT {fields} FROM {table} WHERE namespace_uid = %s AND (start BETWEEN %s AND %s)'

def insert(con, table, data):
    if not isinstance(data, (list, tuple)):
        data = [ data ]
    data = [ i for o in data for i in [[ o[k] for k in FIELD_NAMES[table] ]] ]
    query = make_query('insert', table)
    query = query.format(table, *data[0])
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    cursor.close()


def getsellers(con):
    cursor = con.cursor(cursors.DictCursor)
    query = ('SELECT DISTINCT seller FROM items')
    cursor.execute(query)
    for row in cursor.fetchall():
        yield row
    cursor.close()

def select(con, namespace_uid, start, end):
    cursor = con.cursor(cursors.DictCursor)
    query = SELECT_QUERY.format(table=TABLE_NAME, fields=','.join(FIELD_NAMES[table]))
    print(query % (namespace_uid, start, end))
    cursor.execute(query, (namespace_uid, start, end))
    for row in cursor.fetchall():
        yield row
    cursor.close()

def upsert(con, table, data):
    if not isinstance(data, (list, tuple)):
        data = [ data ]
    data = [ i for o in data for i in [[ o[k] for k in FIELD_NAMES[table] ]] ]
    query = make_query('upsert', table)
    query = query.format(table, *data[0])
    #print(query)
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    cursor.close()