import os
from datetime import datetime
import pymysql.cursors
import requests
import time


connection = pymysql.connect(
    host = "transactionsdb",
    user=os.environ["TRANSACTIONS_DB_USER"],
    password=os.environ["TRANSACTIONS_DB_PASSWORD"],
    db="transaction",
    port = 3315
    )


class order:
    def __init__(self):
        self.conn = connection

    def _execute_order(self, user_id, items):
        cur = self.conn.cursor()
        cur.execute('SELECT MAX(order_id) from db_order;')
        order_id = cur.fetchall()[0][0]
        if not order_id:
            order_id = 1
        else:
            order_id += 1

        self._add_order(order_id, user_id, items, order_status='"pending"')
        total = 100
        if self.__make_payment(user_id, total):
            self._update_order(order_id, order_status='"SUCCESS"')
            status = 200
        else:
            self._update_order(order_id, order_status='"FAIL"')
            status = 400

        cur.close()
        return status


    def _add_order(self, order_id, user_id, items, order_status="pending"):
        cur = self.conn.cursor()
        for item in items:
            try:
                cur.execute(
                    f'''INSERT INTO db_order (order_id, user_id, item_id, price, order_time, order_status)
                    VALUES ({order_id}, {user_id}, '{item[0]}',{item[1]},{"NOW()"},{order_status })''')
                status = 200
            except Exception as e:
                print(e)
                status = 400

        self.conn.commit()
        return status

    def _update_order(self, order_id, order_status):
        cur = self.conn.cursor()
        try:
            cur.execute(
                f'''UPDATE db_order
                SET order_status = {order_status}
                WHERE order_id = {order_id};''')

            status = 200
        except Exception as e:
            print(e)
            status = 400

        self.conn.commit()
        return status

    def __make_payment(self, user_id, amount):
        try:
            time.sleep(3)
            return True
        except:
            return False

class cart:
    def __init__(self):
        self.conn = connection

    def _addCart(self, user_id, item_id):
        price = requests.get(f"http://items:3307/item/get/{item_id}").json()["gotten"]["price"]
        cur = self.conn.cursor()
        try:
            cur.execute(
                f'''INSERT INTO db_cart
                VALUES ('{item_id}', {user_id}, {price}, False, False);''')

            status = 200
        except:
            print("Duplicated key!")
            status = 400

        self.conn.commit()
        cur.close()
        return status

    def _deleteCart(self, user_id, item_id):
        cur = self.conn.cursor()
        try:
            cur.execute(
                f'''DELETE FROM db_cart
                WHERE user_id = {user_id} and item_id = '{item_id}';''')

            status = 200
        except Exception as e:
            print(e)
            status = 400

        self.conn.commit()
        cur.close()
        return status

    def _deleteCart_by_user(self, user_id, buy_Now=False):
        cur = self.conn.cursor()
        if buy_Now:
            try:
                cur.execute(
                    f'''DELETE FROM db_cart
                    WHERE user_id = {user_id} and later = 0;''')

                status = 200
            except Exception as e:
                print(e)
                status = 400
        else:
            try:
                cur.execute(
                    f'''DELETE FROM db_cart
                    WHERE user_id = {user_id};''')

                status = 200
            except Exception as e:
                print(e)
                status = 400

        self.conn.commit()
        cur.close()
        return status

    def _deleteCart_by_item(self, item_id):
        cur = self.conn.cursor()
        try:
            cur.execute(
                f'''DELETE FROM db_cart
                WHERE item_id = '{item_id}';''')

            status = 200
        except Exception as e:
            print(e)
            status = 400

        self.conn.commit()
        cur.close()
        return status

    def _checkout(self, user_id):
        items = self._fetchCart_by_user(user_id)[1]
        if not items:
            status = 400
            return status

        newOrder = order()
        if newOrder._execute_order(user_id, items) == 200:
            self._deleteCart_by_user(user_id=user_id)
            for item in items:
                try:
                    self._deleteCart_by_item(item[0])
                except:
                    pass

            status = 200
        else:
            status = 400

        return status

    def _fetchCart_by_user(self, user_id, buy_now=False):
        cur = self.conn.cursor()
        if buy_now:
            cur.execute(
                f'''SELECT item_id, price
                FROM db_cart
                WHERE user_id = {user_id} and later={False};''')
        else:
            cur.execute(
                f'''SELECT item_id, price
                FROM db_cart
                WHERE user_id = {user_id};''')

        c = cur.fetchall()
        if not c:
            return (400, None)

        item_list =[]
        for x in c:
            item_list.append([x[0], x[1]])

        cur.close()
        return (200, item_list)
