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


conn = connect_to_mysql(host="auctionsdb",
                        user=os.environ["AUCTIONS_DB_USER"],
                        password=os.environ["AUCTIONS_DB_PASSWORD"],
                        db="auctions",
                        port=3328)


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
    # the column names are the caller's own field names and the values can carry
    # form input, so the names are checked and every value is bound
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
    id = cursor.lastrowid
    conn.commit()
    return id
