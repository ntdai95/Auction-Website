import pymysql
from models import User
import crud

class UserDB:
    def __init__(self) -> None:
        self.__connection = pymysql.connect(host="usersdb",
                                            user="user",
                                            password="user",
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
        sql_query = "SELECT * FROM user WHERE "
        conditions = []

        if user_attributes["user_id"]:
            conditions.append(f"user_id = '{user_attributes['user_id']}'")
        if user_attributes["username"]:
            conditions.append(f"username = '{user_attributes['username']}'")
        if user_attributes["password"]:
            conditions.append(f"password = '{user_attributes['password']}'")
        if user_attributes["email"]:
            conditions.append(f"email = '{user_attributes['email']}'")
        if user_attributes["user_type"]:
            conditions.append(f"user_type = '{user_attributes['user_type']}'")
        if user_attributes["user_status"]:
            conditions.append(f"user_status = '{user_attributes['user_status']}'")
        if user_attributes["user_rating_sum"]:
            conditions.append(f"user_rating_sum = '{user_attributes['user_rating_sum']}'")
        if user_attributes["user_rating_total"]:
            conditions.append(f"user_rating_total = '{user_attributes['user_rating_total']}'")
        if user_attributes["watchlist_parameter"]:
            conditions.append(f"watchlist_parameter = '{user_attributes['watchlist_parameter']}'")
        
        if conditions ==[]:
            return None
        for i in range(len(conditions) - 1):
            sql_query += conditions[i] + " AND "
        sql_query += f"{conditions[-1]};"

        cursor = self.__connection.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchone()
        return result
    
    def get_all_users(self,params=None,values=None):
        admins = crud.search('user','user_id',params, values)
        print(admins)
        admins = [self.read_user(User(user_id=i[0])) for i in admins]
        print(f"2.: {admins}")
        return admins

    def create_user(self, user=User):
        user_attributes = user.dict()
        sql_query = "INSERT INTO user (username, password, email, user_type, user_status, user_rating_sum, user_rating_total, watchlist_parameter) " + \
                    f"VALUES ('{user_attributes['username']}', '{user_attributes['password']}', '{user_attributes['email']}', '{user_attributes['user_type']}', " + \
                    f"'{user_attributes['user_status']}', '{user_attributes['user_rating_sum']}', '{user_attributes['user_rating_total']}', " + \
                    f"'{user_attributes['watchlist_parameter']}')"

        cursor = self.__connection.cursor()
        with self.__connection:
            cursor.execute(sql_query)
            self.__connection.commit()
            user_id = cursor.lastrowid
        return user_id

    
    def update_user(self, user=User):
        user_attributes = user.dict()
        sql_query = "UPDATE user SET "
        setters = []
        if user_attributes["username"]:
            setters.append(f"username = '{user_attributes['username']}'")
        if user_attributes["password"]:
            setters.append(f"password = '{user_attributes['password']}'")
        if user_attributes["email"]:
            setters.append(f"email = '{user_attributes['email']}'")
        if user_attributes["user_status"]:
            setters.append(f"user_status = '{user_attributes['user_status']}'")
        if user_attributes["user_rating_sum"]:
            setters.append(f"user_rating_sum = user_rating_sum + '{user_attributes['user_rating_sum']}'")
        if user_attributes["user_rating_total"]:
            setters.append(f"user_rating_total = user_rating_total + '{user_attributes['user_rating_total']}'")
        if user_attributes["watchlist_parameter"]:
            setters.append(f"watchlist_parameter = '{user_attributes['watchlist_parameter']}'")
        
        for i in range(len(setters) - 1):
            sql_query += setters[i] + ", "
        sql_query += f"{setters[-1]} WHERE user_id = '{user_attributes['user_id']}';"

        cursor = self.__connection.cursor()
        with self.__connection:
            result = cursor.execute(sql_query)
            self.__connection.commit()
        return result

    
    def delete_user(self, user=User):
        user_attributes = user.dict()
        sql_query = f"DELETE FROM user WHERE user_id = '{user_attributes['user_id']}'; "

        cursor = self.__connection.cursor()
        with self.__connection:
            result = cursor.execute(sql_query)
            self.__connection.commit()
        return result
