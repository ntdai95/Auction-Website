from os import error
from datetime import datetime
import pymysql.cursors
import time
from functools import reduce
import sys
#from mysql.connector import  MySQLIntegrityConstraintViolationException



connection = pymysql.connect(
    host = "transactionsdb",
    user="transaction",
    password="transaction",
    db="transaction",
    port = 3315
    )


class order:
    ordet_id: int
    order_time: datetime
    user_id: str
    item_id: str
    price: float
    order_status : str

    def __init__(self):
        self.conn = connection
        pass

    def _execute_order(self, user_id, items):
        '''
        Takes: user_id (str), items(items to be bought and its prices)
        Func:   1. Item data are stored in the order database (status = pending)
                2. Payment attempted
                3. If payment successful, item data removed from cart database
        Return: "success!" (str)
        '''
        cur = self.conn.cursor()
        print("execute order is called in order service...", file=sys.stderr)
    
        # Create order id
        cur.execute(f'''SELECT MAX(order_id)  from db_order;
                            ''')
        order_id = cur.fetchall()[0][0]
        if(not order_id):
            order_id = 1
        else:
            order_id += 1
        
        # Add order before payment with pending status
        self._add_order(order_id, user_id, items, order_status  = '"pending"')
        
        # Calculate total price
        # prices = list(map(lambda x:x[1], items))
        # total = reduce(lambda a,b:a+b,prices)
        total = 100
         
        # Make payment and update payment status in the databases
        if(self.__make_payment(user_id, total)):
            self._update_order(order_id, order_status ='"SUCCESS"')
            status = 200
        else:
            self._update_order(order_id, order_status ='"FAIL"')
            status = 400
            
        cur.close()
        print(status,file=sys.stderr)
        return status
    
    
    def _add_order(self, order_id, user_id, items, order_status  = "pending"):
        '''
        Takes: order_id(int), user_id (str), items(items_id and price, dict), status(str)
        Func:  Add order to the database
        Return: None
        '''
        cur = self.conn.cursor()
        for item in items:
            try:
                cur.execute(f'''INSERT INTO db_order (order_id, user_id, item_id, price, order_time, order_status ) VALUES 
                                ({order_id}, {user_id}, '{item[0]}',100,{"NOW()"},{order_status })
                            ''')
                status = 200
            except error as e:
                print(e)
                status = 400
                pass
        self.conn.commit()
    
    
    def _update_order(self, order_id, order_status ):
        '''
        Takes: order_id, order_status (str)
        Func:  Update order_status  of the order (i.e, from "pending" to "success" if payment is done)
        Return: 200 or 400
        '''
        cur = self.conn.cursor()
        try:
            cur.execute(f'''UPDATE db_order SET order_status  = {order_status } 
                            WHERE order_id = {order_id}
                            ''')
            status = 200
        except error as e:
            print(e)
            status = 400
            pass
        self.conn.commit()
        return status


    def __make_payment(self, user_id, amount):
        '''
        Takes: user_id(str), amount(float)
        Func:  Make payment (mocking by waiting for several seconds)
        Return: 200 or 400
        '''
        try:
            time.sleep(3) 
            return True
        except:
            return False

    
    # def _fetchOrder(self):
    #     '''
    #     Takes: None
    #     Return: All orders
    #     '''
    #     cur = self.conn.cursor()
    #     cur.execute(f'''SELECT * FROM db_order;
    #                     ''')
    #     c = cur.fetchall()
    #     if not c:
    #         return (400,None)
    #     cur.close()
    #     return (200,c)


    # def _fetchOrder_by_user(self,user_id):
    #     '''
    #     Takes: user_id
    #     Return: All orders made by the user(dict)
    #     '''
    #     cur = self.conn.cursor()
    #     cur.execute(f'''SELECT * FROM db_order
    #                        WHERE user_id = {user_id};
    #                     ''')
    #     c = cur.fetchall()
    #     if not c:
    #         return (400,None)
        
    #     cur.close()
    #     return (200,c[1])


    # def _fetchOrder_by_item(self,item_id):
    #     '''
    #     Takes: item_id(str)
    #     Return: Orders for the item(dict)
    #     '''
    #     cur = self.conn.cursor()
    #     cur.execute(f'''SELECT * FROM db_order
    #                        WHERE item_id = {item_id};
    #                     ''')
    #     c = cur.fetchall()
    #     if not c:
    #         return (400,None)
        
    #     user_list =[]
    #     for x in c:
    #         user_list.append(x[0])
    #     cur.close()
    #     return (200,user_list)
    
    
    # def _fetchOrder_by_orderid(self,order_id):
    #     '''
    #     Takes: order_id(str)
    #     Return: Orders associated with the order_id(dict)
    #     '''
    #     cur = self.conn.cursor()
    #     cur.execute(f'''SELECT * FROM db_order
    #                        WHERE order_id = {order_id};
    #                     ''')
    #     c = cur.fetchall()
    #     if not c:
    #         return (400,None)
    
    #     cur.close()
    #     return (200,c[1])



class cart:
    user_id: str
    item_id: list
    price: float
    later: bool


    def __init__(self):
        self.conn = connection
        pass


    def _addCart(self, user_id, item_id, price=100, isAuction = False):
        '''
        Takes: user_id(str), item_id(str), price(float), auction(bool)
        Func: Add an an item to the user's cart along with its price
        Return: 200 or 400
        '''
        cur = self.conn.cursor()
        print('addCart in transaction.py',file=sys.stderr)
        print(user_id,file=sys.stderr)
        print(item_id,file=sys.stderr)
        try:
            cur.execute(f'''INSERT INTO db_cart VALUES ('{item_id}', {user_id}, 0, False,False)
                        ''')
            status = 200
        except:
            print("Duplicated key!")
            status = 400
        self.conn.commit()
        cur.close()
        return status


    def _deleteCart(self,user_id, item_id):
        '''
        Takes: user_id(str), item_id(str)
        Func: Delete an an item from the user's cart
        Return: 200 or 400
        '''
        print('deleteCart in transaction.py',file=sys.stderr)
        print(user_id,file=sys.stderr)
        print(item_id,file=sys.stderr)
        cur = self.conn.cursor()
        try:
            cur.execute(f'''DELETE FROM db_cart WHERE user_id = {user_id} and item_id = '{item_id}'
                        ''')
            status = 200
        except error as e:
            print(e)
            status = 400
            pass
        self.conn.commit()
        cur.close()
        print(status)
        
    
    def _deleteCart_by_user(self,user_id, buy_Now=False):
        '''
        Takes: user_id(str)
        Func: Delete user's cart
        Return: 200 or 400
        '''
        cur = self.conn.cursor()
        if(buy_Now): 
            try:
                cur.execute(f'''DELETE FROM db_cart WHERE user_id = {user_id} and later = 0
                            ''')
                status = 200
            except error as e:
                print(e)
                status = 400
        else:
            try:
                cur.execute(f'''DELETE FROM db_cart WHERE user_id = {user_id} 
                            ''')
                status = 200
            except error as e:
                print(e)
                status = 400
        self.conn.commit()
        cur.close()
        print(status)
        pass
    
    def _deleteCart_by_item(self,item_id):
        '''
        Takes: item_id(str)
        Func: Delete the item from all carts
        Return: 200 or 400
        '''
        cur = self.conn.cursor()
        try:
            cur.execute(f'''DELETE FROM db_cart WHERE item_id = '{item_id}' 
                        ''')
            status = 200
        except error as e:
            print(e)
            status = 400
        self.conn.commit()
        cur.close()
        print(status)
        pass

    def _checkout(self,user_id):
        '''
        Takes: user_id(str)
        Func: Execute payment
            1. Get all items that are not marked as "Buy Later" from the user's cart along with its price
            2. Execute order
            3. If successful, delete those items from the cart
             4. If someone else has put the item in their cart, it is deleted as well
        Return: 200 or 400
        '''
        print("checkout in cart called...", file=sys.stderr)
        items = self._fetchCart_by_user(user_id)[1]
        if(not items):
            status = 400
            return status
        newOrder = order()
        if(newOrder._execute_order(user_id, items)):
            self._deleteCart_by_user(user_id=user_id)
            for item in items:
                try:
                    self._deleteCart_by_item(item[0])
                except:
                    pass
                print("all item deleted...", file=sys.stderr)
            status = 200
        else:
            status = 400
        return status

    # def _fetchCart(self):
    #     '''
    #     Takes: NONE
    #     Return: All carts
    #     '''
    #     cur = self.conn.cursor()
    #     cur.execute(f'''SELECT * FROM db_cart;
    #                         ''')
    #     c = cur.fetchall()
    #     if not c:
    #         return (400,None)
    #     cur.close()
    #     return (200,c)
    
    
    def _fetchCart_by_user(self,user_id, buy_now = False):
        '''
        Takes: user_id(str), item_id(str), buy_now(bool, default=false)
        Return: User's cart
        '''
        cur = self.conn.cursor()
        print("fetchCart_by_user was called")
        # If "buy_now" is true, select carts that are not marked as "Buy_later"
        # Otherwise, select all carts of the user
        if(buy_now):
            cur.execute(f'''SELECT item_id, price FROM db_cart
                           WHERE user_id = {user_id} and later={False};
                        ''')     
        else:
            cur.execute(f'''SELECT item_id, price FROM db_cart
                           WHERE user_id = {user_id};
                        ''')
        c = cur.fetchall()
        if not c:
            return (400,None)
        
        item_list =[]
        for x in c:
            item_list.append([x[0],x[1]])
        print("returning...")
        print(item_list)
        cur.close()
        return (200, item_list)


    # def _fetchCart_by_item(self,item_id):
    #     '''
    #     Takes: item_id(str)
    #     Return: All carts containing the item(dict)
    #     '''
    #     cur = self.conn.cursor()
    #     cur.execute(f'''SELECT user_id FROM db_cart
    #                        WHERE item_id = {item_id};
    #                     ''')
    #     c = cur.fetchall()
    #     if not c:
    #         return (400,None)
        
    #     user_list =[]
    #     for x in c:
    #         user_list.append(x[0])
    #     cur.close()
    #     return (200,user_list)
    
    # def _flip_buyLater(self, user_id, item_id):
    #     '''
    #     Takes: NONE
    #     Return: All carts
    #     '''
    #     cur = self.conn.cursor()
    #     c = cur.execute(f'''UPDATE db_cart SET later = {True} 
    #                         WHERE user_id = {user_id} and item_id = {item_id} and auction = 0
    #                         ''')
    #     self.conn.commit()
    #     cur.close()
    #     return (200)
    
    # def _flip_buyNow(self, user_id, item_id):
    #     '''
    #     Takes: NONE
    #     Return: All carts
    #     '''
    #     cur = self.conn.cursor()
    #     cur.execute(f'''UPDATE db_cart SET later = {False}
    #                         WHERE user_id = {user_id} and item_id = {item_id}
    #                         ''')
    #     self.conn.commit()
    #     cur.close()
    #     return (200)
    




