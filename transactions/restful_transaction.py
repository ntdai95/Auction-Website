from flask import Flask, jsonify, request
from transaction import cart


app = Flask(__name__)


@app.route("/cart/getCart_by_user", methods=['GET'])
def getCart_by_user():
    if request.method == 'GET':
        user = request.args.get('user_id')
        items = cart()._fetchCart_by_user(user_id=user)
        return (jsonify(items[1]))

    return jsonify("Bad Request")

@app.route("/cart/addCart/<item>/<user>", methods=['GET'])
def addCart(item,user):
    if request.method == 'GET':
        c = cart()._addCart(user_id=user,item_id=item)
        if c == 400:
            return jsonify("Item already in a cart!")

        cart()._fetchCart_by_user(user_id=user)
        return jsonify("success!")

    return jsonify("Bad Request")

@app.route("/cart/executeOrder", methods=['POST'])
def executeOrder():
    if request.method == 'POST':
        user = request.args.get('user_id')
        c = cart()._checkout(user_id=user)
        if c == 400:
            return jsonify("Checkout Failed")

        return jsonify("SUCCESS")

    return jsonify("Bad Request")

@app.route("/cart/deleteCart/<item>/<user>", methods=['DELETE'])
def deleteCart(item, user):
    if request.method == 'DELETE':
        cart()._deleteCart(user_id=user, item_id=item)
        return jsonify("success")

    return jsonify("Bad Request")

@app.route("/cart/deleteCart_byItem", methods=['DELETE'])
def deleteCart_byItem():
    if request.method == 'DELETE':
        item = request.args.get('item_id')
        cart()._deleteCart_by_item(item_id=item)
        return jsonify("success")

    return jsonify("Bad Request")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3305, debug=True)
