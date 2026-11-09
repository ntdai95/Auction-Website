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


def create(table, inputs):
    # the column names are the caller's dataclass fields, but the values can
    # carry form input, so they are bound rather than pasted into the statement
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
    id = cursor.lastrowid
    conn.commit()
    return id
