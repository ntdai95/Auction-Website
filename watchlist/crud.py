import datetime
import os
import time
import pymysql.cursors

conn = pymysql.connect(host="watchlistdb",
                       user=os.environ["WATCHLIST_DB_USER"],
                       password=os.environ["WATCHLIST_DB_PASSWORD"],
                       db="watchlist",
                       port=3321)

def create(table, inputs):
    values = []
    for i in inputs.values():
        if type(i) == str:
            values.append(f"\"{i}\"")
        elif not i:
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
    WHERE {primary_key} = {key_value};
    """
    cursor = conn.cursor()
    cursor.execute(delete)
    conn.commit()

def read(table, primary_key, key_value, columns=None):
    cols = None
    if type(key_value) == str:
        key_value = "\"" + key_value + "\""

    if columns:
        cols = ','.join(columns)

    get = \
    f"""
    SELECT {cols or "*"}
    FROM {table}
    WHERE {primary_key} = {key_value};
    """
    cursor = conn.cursor()
    cursor.execute(get)
    return cursor.fetchall()

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
    for a, b in zip(properties, values):
        if a =='price':
            min, max = b
            s = f"{a} BETWEEN {min} AND {max}"
        else:
            s = f"{a} LIKE \'%{b}%\'"

        search_keys.append(s)

    search = \
    f"""
    SELECT {primary_key}
    FROM {table}
    WHERE {" AND ".join(search_keys)};
    """
    cursor = conn.cursor()
    cursor.execute(search)
    return cursor.fetchall()
