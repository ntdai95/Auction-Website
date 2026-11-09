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


def update(table, primary_key, key_value, column, column_value):
    if type(key_value) == str:
        key_value = "\"" + key_value + "\""

    if type(column_value) == str:
        column_value = "\"" + column_value + "\""

    if column_value is None:
        column_value = "NULL"

    if type(column_value) == datetime.datetime:
        column_value = time.strftime('%Y-%m-%d %H:%M:%S', column_value.timetuple())

    update = \
    f"""
    UPDATE {table}
    SET {column} = {column_value}
    WHERE {primary_key} = {key_value};
    """
    cursor = conn.cursor()
    cursor.execute(update)
    conn.commit()

def batch_update(table, primary_key, key_value, columns=[], column_values=[]):
    values = []
    for i in column_values:
        bls =  ["False", "True", False, True]
        if i in bls:
            v = bls.index(i) % 2
            values.append(str(bool(v)))
        elif type(i) == str:
            values.append(f"\"{i}\"")
        elif type(i) == list:
            val = ' | '.join(i)
            values.append(val)
        else:
            values.append(str(i))

    paired = ""
    for i, col in enumerate(columns):
        p = col + "=" + (values[i] or "NULL")
        paired += p + ","

    paired = paired.strip(",")
    if type(key_value) == str:
        key_value = "\"" + key_value + "\""

    update= \
    f"""
    UPDATE {table}
    SET {paired}
    WHERE {primary_key} ={key_value};
    """
    cursor = conn.cursor()
    cursor.execute(update)
    conn.commit()

def create(table, inputs):
    values = []
    for i in inputs.values():
        if type(i) == str:
            values.append(f"\"{i}\"")
        elif i is None:
            values.append("NULL")
        elif type(i) == datetime.datetime:
            dte = time.strftime('%Y-%m-%d %H:%M:%S', datetime.datetime.utcnow().timetuple())
            values.append("\"" + str(dte) + "\"")
        else:
            values.append(str(i))

    values = ",".join(values)
    insert = \
    f"""
    INSERT INTO {table} ({",".join(inputs.keys())})
    VALUES ({values});
    """
    cursor = conn.cursor()
    cursor.execute(insert)
    conn.commit()

def delete(from_table, primary_key, key_value):
    if type(key_value) == str:
        key_value = "\"" + key_value + "\""

    delete = \
    f"""
    DELETE FROM {from_table}
    WHERE {primary_key}={key_value};
    """
    cursor = conn.cursor()
    cursor.execute(delete)
    conn.commit()

def read(table, primary_key, key_value, columns=None, as_dict=False):
    cols = None
    if type(key_value) == str:
        key_value = "\"" + key_value + "\""

    if columns:
        cols = ','.join(columns)

    get = \
    f"""
    SELECT {cols or "*"}
    FROM {table}
    WHERE
        {primary_key} = {key_value}
    """
    cursor = conn.cursor()
    cursor.execute(get)
    rows = cursor.fetchall()
    if as_dict:
        names = [d[0] for d in cursor.description]
        return [dict(zip(names, row)) for row in rows]

    return rows

def search(table, primary_key, properties, search_values):
    values = []
    for i in search_values:
        if not i:
            values.append("NULL")
        elif type(i) == datetime.datetime:
            dte = time.strftime('%Y-%m-%d %H:%M:%S', datetime.datetime.utcnow().timetuple())
            values.append("\"" + str(dte) + "\"")
        else:
            values.append(str(i))

    search_keys = []
    for i in zip(properties, values):
        a, b = i
        if a == 'price':
            min, max = b
            s = f"{a} BETWEEN {min} AND {max}"
        else:
            s = f"{a} LIKE \'%{b}%\'"

        search_keys.append(s)

    search = \
    f"""
    SELECT {primary_key}
    FROM {table}
    WHERE {" AND ".join(search_keys)} AND sold = 0;
    """
    cursor = conn.cursor()
    cursor.execute(search)
    return cursor.fetchall()
