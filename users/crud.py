import datetime
import time
import pymysql.cursors

conn = pymysql.connect(host="usersdb",
                       user="user",
                       password="user",
                       db="user",
                       port=3322)

def update(table, primary_key, key_value, column,
                 column_value):
    '''
        Update a single row from {table} where 
        the column {primary_key} equals {key_value} 
        setting the value for column {column} to {column_value}.
    '''
    if type(key_value)==str:
        key_value = "\"" + key_value + "\""
    if type(column_value)==str:
        column_value = "\"" + column_value + "\""
    if column_value==None:
        column_value="NULL"
    if type(column_value)==datetime:
        column_value = time.strftime('%Y-%m-%d %H:%M:%S', column_value.timetuple())
        
    update = \
    f"""
    UPDATE {table}
    SET 
        {column} = {column_value}
    WHERE 
        {primary_key} = {key_value};
    """
    cursor = conn.cursor()
    cursor.execute(update)
    conn.commit()

def batch_update(table, primary_key, key_value, columns: list=[],column_values: list = []):
    values = []
    for i in column_values:
        bls =  ["False","True",False, True]
        if i in bls:
            v = bls.index(i) % 2
            values.append(str(bool(v)))
        elif type(i) == str:
            values.append(f"\"{i}\"")
        elif type(i)==list:
            val = ' | '.join(i)
            values.append(val)
        else:
            values.append(str(i))
    print(f"""
    keys {columns} \n
    values {values}
    """)
    paired = ""
    for i,col in enumerate(columns):
        p = col + "=" + (values[i] or "NULL")
        paired+=p+","
    paired = paired.strip(",")
    

    if type(key_value)==str:
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
    """
    table is the tab name
    inputs are a dict of column-value pairs
    """
    values = []
    for i in inputs.values():
        if type(i) == str:
            values.append(f"\"{i}\"")
        elif i==None:
            values.append("NULL")
        elif type(i)==datetime.datetime:
            dte = time.strftime('%Y-%m-%d %H:%M:%S', datetime.datetime.utcnow().timetuple())
            values.append("\""+str(dte)+"\"")
        else:
            values.append(str(i))
    values = ",".join(values)
    
    insert = \
    f"""
    INSERT INTO {table} ({",".join(inputs.keys())})
    VALUES ({values});
    """
    print(insert)

    cursor = conn.cursor()
    cursor.execute(insert)
    conn.commit()

def delete(from_table, primary_key, key_value):
    """
        from_table, to_table, primary_key, key_value
    """
    if type(key_value)==str:
        key_value = "\"" + key_value + "\""
    '''
    archive_date = time.strftime('%Y-%m-%d %H:%M:%S', datetime.datetime.utcnow().timetuple())
    copy = \
    f"""
    INSERT INTO {to_table}
    SELECT *, \'{}\' as archive_date FROM {from_table} 
    WHERE {primary_key}={key_value};
    '''

    delete = \
    f"""
    DELETE FROM {from_table}
    WHERE {primary_key}={key_value};
    """
    cursor = conn.cursor()
    #cursor.execute(copy)
    cursor.execute(delete)
    conn.commit()

def read(table, primary_key, key_value, columns: list =None):
    """
        Inputs: table, primary_key, key_value, columns as list
    """
    cols=None
    if type(key_value)==str:
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
    return cursor.fetchall()

def search(table, primary_key, properties, search_values):
    """
    """
    values = []
    for i in search_values:
        #if type(i) == str:
        #    values.append(f"\"{i}\"")
        if i==None:
            values.append("NULL")
        elif type(i)==datetime.datetime:
            dte = time.strftime('%Y-%m-%d %H:%M:%S', datetime.datetime.utcnow().timetuple())
            values.append("\""+str(dte)+"\"")
        else:
            values.append(str(i))
    search_keys = []
    for i in zip(properties, values):
        a,b = i
        if a=='price':
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
    print(search)
    cursor = conn.cursor()
    cursor.execute(search)
    return cursor.fetchall()

