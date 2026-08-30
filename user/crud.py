import datetime
import os
import time
import pymysql.cursors

conn = pymysql.connect(host="usersdb",
                       user=os.environ["USERS_DB_USER"],
                       password=os.environ["USERS_DB_PASSWORD"],
                       db="user",
                       port=3322)

def search(table, primary_key, properties, search_values):
    values = []
    for i in search_values:
        if i == None:
            values.append("NULL")
        elif type(i) == datetime.datetime:
            dte = time.strftime('%Y-%m-%d %H:%M:%S', datetime.datetime.utcnow().timetuple())
            values.append("\"" + str(dte) + "\"")
        else:
            values.append(str(i))

    search_keys = []
    for a, b in zip(properties, values):
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
    WHERE {" AND ".join(search_keys)};
    """
    cursor = conn.cursor()
    cursor.execute(search)
    return cursor.fetchall()
