import datetime
import os
import time
import pymysql.cursors


conn = pymysql.connect(host="auctionsdb",
                       user=os.environ["AUCTIONS_DB_USER"],
                       password=os.environ["AUCTIONS_DB_PASSWORD"],
                       db="auctions",
                       port=3328)


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
    id = cursor.lastrowid
    conn.commit()
    return id
