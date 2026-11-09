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


conn = connect_to_mysql(host="watchlistdb",
                        user=os.environ["WATCHLIST_DB_USER"],
                        password=os.environ["WATCHLIST_DB_PASSWORD"],
                        db="watchlist",
                        port=3321)


# Every value below is bound as a parameter. Column and table names cannot be
# bound, so any that could come from request data are checked against the
# table's real columns before they reach a statement.

_column_cache = {}


def _known_columns(table):
    if table not in _column_cache:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_schema = DATABASE() AND table_name = %s",
            (table,))
        _column_cache[table] = {row[0].lower() for row in cursor.fetchall()}

    return _column_cache[table]


def _check_identifiers(table, columns):
    known = _known_columns(table)
    for column in columns:
        if str(column).lower() not in known:
            raise ValueError(f"unknown column {column!r} for table {table!r}")


def create(table, inputs):
    columns = list(inputs.keys())
    _check_identifiers(table, columns)
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
    WHERE {primary_key} = %s;
    """
    cursor = conn.cursor()
    cursor.execute(delete, (key_value,))
    conn.commit()

def read(table, primary_key, key_value, columns=None):
    cols = ','.join(columns) if columns else "*"

    get = \
    f"""
    SELECT {cols}
    FROM {table}
    WHERE {primary_key} = %s;
    """
    cursor = conn.cursor()
    cursor.execute(get, (key_value,))
    return cursor.fetchall()

def search(table, primary_key, properties, search_values):
    _check_identifiers(table, properties)
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
