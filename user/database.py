import os
import pymysql
from models import User
import crud

class UserDB:
    def __init__(self):
        self.__connection = pymysql.connect(host="usersdb",
                                            user=os.environ["USERS_DB_USER"],
                                            password=os.environ["USERS_DB_PASSWORD"],
                                            db="user",
                                            port=3322)
        self.__create_table()
    

    def __create_table(self):
        cursor = self.__connection.cursor()
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS user (
                            user_id INT NOT NULL AUTO_INCREMENT,
                            username TEXT,
                            password TEXT,
                            email TEXT,
                            user_type TEXT,
                            user_status TEXT,
                            user_rating_sum INT,
                            user_rating_total INT,
                            watchlist_parameter TEXT,
                            PRIMARY KEY (user_id)
                        );""")
    
    
    ############################################
    #            USER TABLE QUERIES            #
    ############################################


    def read_user(self, user=User):
        user_attributes = user.dict()
        # the login form reaches here with an unauthenticated username, so the
        # value is bound as a parameter rather than pasted into the statement
        columns = ["user_id", "username", "password", "email", "user_type",
                   "user_status", "user_rating_sum", "user_rating_total",
                   "watchlist_parameter"]
        conditions = []
        params = []
        for column in columns:
            if user_attributes[column]:
                conditions.append(f"{column} = %s")
                params.append(user_attributes[column])

        if not conditions:
            return None

        sql_query = "SELECT * FROM user WHERE " + " AND ".join(conditions) + ";"

        cursor = self.__connection.cursor()
        cursor.execute(sql_query, params)
        result = cursor.fetchone()
        return result
    
    def get_all_users(self,params=None,values=None):
        admins = crud.search('user','user_id',params, values)
        admins = [self.read_user(User(user_id=i[0])) for i in admins]
        return admins

    def create_user(self, user=User):
        user_attributes = user.dict()
        columns = ["username", "password", "email", "user_type", "user_status",
                   "user_rating_sum", "user_rating_total", "watchlist_parameter"]
        sql_query = ("INSERT INTO user (" + ", ".join(columns) + ") "
                     "VALUES (" + ", ".join(["%s"] * len(columns)) + ")")
        params = [user_attributes[column] for column in columns]

        cursor = self.__connection.cursor()
        with self.__connection:
            cursor.execute(sql_query, params)
            self.__connection.commit()
            user_id = cursor.lastrowid
        return user_id

    
    def update_user(self, user=User):
        user_attributes = user.dict()
        # the two rating columns accumulate, so their placeholder is the amount
        # added rather than the whole clause
        setters_by_column = {
            "username": "username = %s",
            "password": "password = %s",
            "email": "email = %s",
            "user_status": "user_status = %s",
            "user_rating_sum": "user_rating_sum = user_rating_sum + %s",
            "user_rating_total": "user_rating_total = user_rating_total + %s",
            "watchlist_parameter": "watchlist_parameter = %s",
        }
        setters = []
        params = []
        for column, clause in setters_by_column.items():
            if user_attributes[column]:
                setters.append(clause)
                params.append(user_attributes[column])

        sql_query = "UPDATE user SET " + ", ".join(setters) + " WHERE user_id = %s;"
        params.append(user_attributes["user_id"])

        cursor = self.__connection.cursor()
        with self.__connection:
            result = cursor.execute(sql_query, params)
            self.__connection.commit()
        return result

    
    def delete_user(self, user=User):
        user_attributes = user.dict()
        sql_query = "DELETE FROM user WHERE user_id = %s;"

        cursor = self.__connection.cursor()
        with self.__connection:
            result = cursor.execute(sql_query, [user_attributes["user_id"]])
            self.__connection.commit()
        return result
