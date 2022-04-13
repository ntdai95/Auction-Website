from flask import Flask, jsonify, request
from transaction import cart
import sys

app = Flask(__name__)

@app.route("/cart")
@app.route("/cart/getCart_by_user", methods=['GET'])
def getCart_by_user():
    '''
    Takes: user_id (str)
    Return: Cart of the user (dict) # A list of items that the user has put in the cart
    '''
    if request.method=='GET':
        print("we got a get request")
        user = request.args.get('user_id')
        print(f"{user} was received")
        items = cart()._fetchCart_by_user(user_id=user)
        print("rest returns...")
        print(items[1])
        return (jsonify(items[1]))
    return jsonify("Bad Request")


@app.route("/cart")
@app.route("/cart/addCart/<item>/<user>", methods=['GET'])
def addCart(item,user):
    '''
    Takes: user_id (str), item_id (str)
    Func: Add an item in the user's cart
    Return: "success" (str)
    '''
    print(item,user,file=sys.stderr)
    if request.method=='GET':
        # user = request.args.get('user_id')
        # item = request.args.get('item_id')
        c = cart()._addCart(user_id=user,item_id=item)
        if(c==400):
            return jsonify("Item already in a cart!")
        items = cart()._fetchCart_by_user(user_id=user)
        return jsonify("success!")
    return jsonify("Bad Request")



@app.route("/cart")
@app.route("/cart/executeOrder", methods=['POST'])
def executeOrder():
    '''
    Takes: user_id (str)
    Func: Call Checkout 
            1. Item data are stored in the order database
            2. Payment attempted
            3. If payment successful, item data removed from cart database
            4. If someone else has put the item in their cart, it is deleted
    Return: "success" (str)
    '''
    if request.method=='POST':
        user = request.args.get('user_id')
        print("execute order...", file=sys.stderr)
        c = cart()._checkout(user_id=user)
        if(c==400):
            print("Checkout failed...", file=sys.stderr)
            return jsonify("Checkout Failed")
        #item/edit
        return jsonify("SUCCESS")
    return jsonify("Bad Request")


@app.route("/cart")
@app.route("/cart/deleteCart/<item>/<user>", methods=['DELETE'])
def deleteCart(item, user):
    '''
    Takes: user_id (str),item_id (str)
    Func: Delete item from the cart
    Return: "success" (str)
    '''
    if request.method=='DELETE':
        # user = request.args.get('user_id')
        # item = request.args.get('item_id')
        c = cart()._deleteCart(user_id=user, item_id=item)
        return jsonify("success")
    return jsonify("Bad Request")


@app.route("/cart")
@app.route("/cart/deleteCart_byItem", methods=['DELETE'])
def deleteCart_byItem():
    '''
    Takes: user_id (str),item_id (str)
    Func: Delete item from the cart
    Return: "success" (str)
    '''
    if request.method=='DELETE':
        item = request.args.get('item_id')
        c = cart()._deleteCart_by_item(item_id=item)
        return jsonify("success")
    return jsonify("Bad Request")







if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=3305, debug = True)

#################################
#Codes that are not currently used
# @app.route("/cart")
# @app.route("/cart/getCart", methods=['GET'])
# def getCart():
#     '''
#     Takes: NONE
#     Return: All carts (dict)
#     '''
#     if request.method=='GET':
#         carts = cart()._fetchCart()
#         return jsonify(carts[1])
#     return jsonify("Bad Request")


# @app.route("/cart")
# @app.route("/cart/getCart_by_item", methods=['GET'])
# def getCart_by_item():
#     '''
#     Takes: item_id (str)
#     Return: Cart that has the item in it (dict) # A list of users that has put the item in the cart
#     '''
#     if request.method=='GET':
#         item = request.args.get('item_id')
#         users = cart()._fetchCart_by_item(item_id=item)
#         return jsonify(users[1])
#     return jsonify("Bad Request")

# @app.route("/cart")
# @app.route("/cart/addCart_auction", methods=['GET'])
# def addCart_auction():
#     '''
#     Takes: user_id (str), item_id (str), price(float)
#     Func: Add an auction item in the user's cart
#     Return: "success" (str)
#     '''
#     if request.method=='GET':
#         user = request.args.get('user_id')
#         item = request.args.get('item_id')
#         price = request.args.get('price')
#         c = cart()._addCart(user_id=user,item_id=item, price = price, isAuction = True)
#         if(c==400):
#             return jsonify("Item already in a cart!")
#         items = cart()._fetchCart_by_user(user_id=user)
#         return jsonify("success")
#     return jsonify("Bad Request")


# @app.route("/cart")
# @app.route("/cart/deleteCart_byUser", methods=['DELETE'])
# def deleteCart_byUser():
#     '''
#     Takes: user_id (str),item_id (str)
#     Func: Delete item from the cart
#     Return: "success" (str)
#     '''
#     if request.method=='DELETE':
#         user = request.args.get('user_id')
#         c = cart()._deleteCart_by_user(user_id = user)
#         return jsonify("success")
#     return jsonify("Bad Request")


# @app.route("/cart")
# @app.route("/cart/buyLater", methods=['POST'])
# def buyLater():
#     '''
#     Takes: user_id (str),item_id (str)
#     Func: If the item is marked as "buy now", make it "buy later", UNLESS it is bought from auction
#     Return: "success" (str)
#     '''
#     if request.method=='POST':
#         user = request.args.get('user_id')
#         item = request.args.get('item_id')
#         c = cart()._flip_buyLater(user_id=user, item_id=item)
#         return jsonify(c)
#     return jsonify("Bad Request")


# @app.route("/cart")
# @app.route("/cart/buyNow", methods=['POST'])
# def buyNow():
#     '''
#     Takes: user_id (str),item_id (str)
#     Func: If the item is marked as "buy later", make it "buy now"
#     Return: "success" (str)
#     '''
#     if request.method=='POST':
#         user = request.args.get('user_id')
#         item = request.args.get('item_id')
#         c = cart()._flip_buyNow(user_id=user, item_id=item)
#         return jsonify(c)
#     return jsonify("Bad Request")

# @app.route("/order")
# @app.route("/order/getOrder", methods=['GET'])
# def getOrder():
#     '''
#     Takes: NONE
#     Return: List of any orders(dict)
#     '''
#     if request.method=='GET':
#         orders = order()._fetchOrder()
#         return jsonify(orders[1])
#     return jsonify("Bad Request")

# @app.route("/order")
# @app.route("/order/getOrder_by_item", methods=['GET'])
# def getOrder_by_item():
#     '''
#     Takes: item_id(str)
#     Return: Order that contains the item(dict)
#     '''
#     if request.method=='GET':
#         item = request.args.get('item_id')
#         users = order()._fetchOrder_by_item(item_id=item)
#         return jsonify(users[1])
#     return jsonify("Bad Request")


# @app.route("/order")
# @app.route("/order/getOrder_by_user", methods=['GET'])
# def getOrder_by_user():
#     '''
#     Takes: user_id(str)
#     Return: List of orders of the user(dict)
#     '''
#     if request.method=='GET':
#         user = request.args.get('user_id')
#         items = order()._fetchOrder_by_user(user_id=user)
#         return jsonify(items[1])
#     return jsonify("Bad Request")

# @app.route("/order/getOrder_by_orderid", methods=['GET'])
# def getOrder_by_orderid():
#     '''
#     Takes: order_id(str)
#     Return: List of orders associated with the order_id(dict)
#     '''
#     if request.method=='GET':
#         order_id = request.args.get('order_id')
#         orders = order()._fetchOrder_by_orderid(order_id=order_id)
#         return jsonify(orders[1])
#     return jsonify("Bad Request")