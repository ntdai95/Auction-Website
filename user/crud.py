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


conn = connect_to_mysql(host="usersdb",
                        user=os.environ["USERS_DB_USER"],
                        password=os.environ["USERS_DB_PASSWORD"],
                        db="user",
                        port=3322)


# the column and table names are the caller's own field names, not request data,
# so they stay in the statement; every value is bound as a parameter


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
    WHERE {" AND ".join(search_keys)};
    """
    cursor = conn.cursor()
    cursor.execute(search, params)
    return cursor.fetchall()
