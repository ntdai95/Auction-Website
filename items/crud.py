import datetime
import os
import time
import pymysql.cursors


def connect_to_mysql(attempts=30, delay=2, **kwargs):
    """Open a MySQL connection, waiting for the server to accept them.

    The database container is started by the same compose file as this
    service and takes a while to initialise on a cold start.

    Args:
        attempts: how many times to try before giving up
        delay: seconds to wait between tries
        kwargs: the connection settings handed to pymysql
    Returns:
        an open pymysql connection
    """
    for attempt in range(1, attempts + 1):
        try:
            return pymysql.connect(**kwargs)
        except pymysql.err.OperationalError:
            if attempt == attempts:
                raise
            print("%s not ready yet, retrying in %ss (%s/%s)"
                  % (kwargs.get("host"), delay, attempt, attempts), flush=True)
            time.sleep(delay)


conn = connect_to_mysql(host="itemsdb",
                        user=os.environ["ITEMS_DB_USER"],
                        password=os.environ["ITEMS_DB_PASSWORD"],
                        db="items",
                        port=3317)


# The column and table names below are the caller's own field names, not request
# data, so they stay in the statement. Every value is bound as a parameter.


def update(table, primary_key, key_value, column, column_value):
    if type(column_value) == datetime.datetime:
        column_value = time.strftime('%Y-%m-%d %H:%M:%S', column_value.timetuple())

    update = \
    f"""
    UPDATE {table}
    SET {column} = %s
    WHERE {primary_key} = %s;
    """
    cursor = conn.cursor()
    cursor.execute(update, (column_value, key_value))
    conn.commit()

def batch_update(table, primary_key, key_value, columns=[], column_values=[]):
    params = []
    for i in column_values:
        bls = ["False", "True", False, True]
        if i in bls:
            params.append(bls.index(i) % 2)
        elif type(i) == list:
            params.append(' | '.join(i))
        else:
            params.append(i)

    paired = ",".join(f"{col}=%s" for col in columns)
    update = \
    f"""
    UPDATE {table}
    SET {paired}
    WHERE {primary_key} = %s;
    """
    params.append(key_value)
    cursor = conn.cursor()
    cursor.execute(update, params)
    conn.commit()

def create(table, inputs):
    columns = list(inputs.keys())
    params = list(inputs.values())
    placeholders = ",".join(["%s"] * len(columns))
    insert = \
    f"""
    INSERT INTO {table} ({",".join(columns)})
    VALUES ({placeholders});
    """
    cursor = conn.cursor()
    cursor.execute(insert, params)
    conn.commit()

def delete(from_table, primary_key, key_value):
    delete = \
    f"""
    DELETE FROM {from_table}
    WHERE {primary_key}=%s;
    """
    cursor = conn.cursor()
    cursor.execute(delete, (key_value,))
    conn.commit()

def read(table, primary_key, key_value, columns=None, as_dict=False):
    cols = ','.join(columns) if columns else "*"

    get = \
    f"""
    SELECT {cols}
    FROM {table}
    WHERE
        {primary_key} = %s
    """
    cursor = conn.cursor()
    cursor.execute(get, (key_value,))
    rows = cursor.fetchall()
    if as_dict:
        names = [d[0] for d in cursor.description]
        return [dict(zip(names, row)) for row in rows]

    return rows

def search(table, primary_key, properties, search_values):
    search_keys = []
    params = []
    for a, b in zip(properties, search_values):
        if a == 'price':
            low, high = b
            search_keys.append(f"{a} BETWEEN %s AND %s")
            params.extend([low, high])
        else:
            search_keys.append(f"{a} LIKE %s")
            params.append(f"%{b}%")

    search = \
    f"""
    SELECT {primary_key}
    FROM {table}
    WHERE {" AND ".join(search_keys)} AND sold = 0;
    """
    cursor = conn.cursor()
    cursor.execute(search, params)
    return cursor.fetchall()
