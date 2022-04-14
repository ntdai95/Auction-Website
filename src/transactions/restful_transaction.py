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
    if request.method == 'GET':
        user = request.args.get('user_id')
        items = cart()._fetchCart_by_user(user_id=user)
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
    if request.method == 'GET':
        c = cart()._addCart(user_id=user,item_id=item)
        if c == 400:
            return jsonify("Item already in a cart!")

        cart()._fetchCart_by_user(user_id=user)
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
    if request.method == 'POST':
        user = request.args.get('user_id')
        c = cart()._checkout(user_id=user)
        if c == 400:
            return jsonify("Checkout Failed")

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
    if request.method == 'DELETE':
        cart()._deleteCart(user_id=user, item_id=item)
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
    if request.method == 'DELETE':
        item = request.args.get('item_id')
        cart()._deleteCart_by_item(item_id=item)
        return jsonify("success")

    return jsonify("Bad Request")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3305, debug=True)
