from flask import Flask, jsonify, request
from flask_restful import Api, reqparse
from item import Item, Categories, COUNTERFEIT_THRESHOLD
import os
import sys

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('list', type=list)

@app.route("/item/test",methods=['GET','POST'])
def test():
    return jsonify("SUCCESS")

"""---INCOMING REQUESTS--->""" 
@app.route("/item/get/<item_id>", methods=['GET'])
def item(item_id):
    """
    takes item_id 
    reuturns: dict of item
    """
    try:
        item = Item.load(item_id)
        print(item)
        return jsonify({"gotten":item})
    except:
        return jsonify({"status": "fail","message":"Bad Request"})

# @app.route("/item/delete/<item_id>", methods=['DELETE'])
@app.route("/item/delete", methods=['DELETE','GET'])
def item_delete():
    '''
    Input: user_id (int), item_id(int)
    Func: Delete the item
    Return: message(str), item_id(str)
    '''
    if True:
        item_id = request.args.get('item_id',None)
        Item.remove_item(item_id)
        return jsonify({"deleted":item_id})
    return jsonify("Bad Request")

@app.route("/item/report_counterfeit", methods=['GET','POST'])
def report_counterfeit():
    '''
    Input: item_id(str)
    Func: Flag item as counterfeit
    Return: None
    '''
    if True:
        item_id = request.args.get('item_id',None)
        item = Item.load(item_id)
        item.set_counterfeit_flag()
        return jsonify('success')
    return jsonify('failed')

@app.route("/item/unflag_counterfeit", methods=['POST','GET'])
def unflag_counterfeit():
    '''
    Input: item_id(str)
    Func: Unflag item as counterfeit
    Return: None
    '''
    if True:
        item_id = request.args.get('item_id',None)
        item = Item.load(item_id)
        item.remove_counterfeit_flag()
        return jsonify('success')
    return jsonify('failed')
@app.route("/item/report_inappropriate", methods=['POST','GET'])
def report_inappropriate():
    '''
    Input: item_id(str)
    Func: Flag item as inappropriate
    Return: None
    '''
    if True:
        item_id = request.args.get('item_id',None)
        item = Item.load(item_id)
        item.set_inappropriate_flag()
        return jsonify('success')
    return jsonify('failed')

@app.route("/item/unflag_inappropriate", methods=['POST','GET'])
def unflag_inappropriate():
    '''
    Input: item_id(str)
    Func: Unflag item as inappropriate
    Return: None
    '''
    if True:

        item_id = request.args.get('item_id',None)
        item = Item.load(item_id)
        item.remove_inappropriate_flag()
        return jsonify('success')
    return jsonify('failed')

@app.route("/item/create", methods=['POST'])
def create_item():
    '''
    Input: properties(list)
    Func: Create an item
    Return: message(str), item(item), item_id(str)
    '''
    if request.method=="POST":
        item = Item()
        
        if request.args.getlist('properties'):
            item.write()
            properties = request.args.getlist('properties')
            values = request.args.getlist('values')
            #properties.append('item_id') 
            #values.append(item.item_id)
            item = item.batch_edit(properties,values)
            if item.price>COUNTERFEIT_THRESHOLD:
                #item.check_counterfeit()
                #item sends notification to admin for counterfeit
                pass
        elif request.args.getlist('empty'):
            item.write()
        else:
            return jsonify({'error':""})
        return jsonify({'created': item.item_id})


@app.route("/item/edit", methods=['POST'])
def edit_item():
    '''
    Input: properties(list), values(list), item_id(str)
    Func: Edit item
    Return: message(str), item(item), item_id(str)
    '''
    properties = request.args.getlist('properties')
    values = request.args.getlist('values')
    item_id = request.args.get('item_id',None)

    item = Item.load(item_id)
    user_id = request.args.get('user_id',None)

    res = item.batch_edit(properties,values)
    print(res,file=sys.stderr)
    #return jsonify({'error':""})
    return jsonify({'edited':item.item_id})

@app.route("/item/inappropriate/", methods= ['GET'])
def check_inappropriateness(item_id):
    '''
    Input: item_id(str)
    Func: Check if item is inappropriate or not
    Return: item.check_inappropriateness() (bool)
    '''
    if request.method=='GET':
        item_id = request.args.get('item_id',None)
        item = Item.load(item_id)
        return jsonify(item.check_inappropriateness())

@app.route("/items/flagged", methods=['GET'])
def view_flagged_items():
    '''
    Input: user_id(str)
    Func: View particular user's flagged item
    Return: Item.view_flagged_items() (list)
    '''
    user = request.args.get('user_id', None)
    field = request.args.get('field', None)
    if user != None:
        return jsonify(Item.view_flagged_items(user,field))
    else:
        return jsonify(Item.view_flagged_items(field=field))
       
@app.route("/items/allitems", methods=['GET'])
def getitems():
    '''
    Input: user_id(str)
    Func: Get all items of the user
    Return: items (list)
    '''
    user_id = request.args.get('user_id',None)
    print(f"[REQUEST FOR] {user_id}")
    item_ids = Item.search_for_item(params=['user_id'],values=[user_id])
    items = []
    for i in item_ids:
        x = vars(Item.load(i))
        items.append(x)
    return jsonify({'items': items})

@app.route("/items/search", methods=['GET'])
def search():
    '''
    Input: params(list), values(list)
    Func: Get all items of the user
    Return: items (list)
    '''
    params = request.args.getlist('params')
    values = request.args.getlist('values')
    print(f"[Search for] {params} {values}")
    item_ids = Item.search_for_item(params=params,values=values)
    items = []
    for i in item_ids:
        x = vars(Item.load(i))
        items.append(x)
    return jsonify({'items': items})


#Outgoing
def is_user_admin(user_id, pword):
    """
    MS: Users
    """
    parameters = {"user_id": user_id}
    result = requests.get("http://users:3312/admin/checkadmin",params=parameters)
    return result.json()['isAdmin']

# Incoming: Category routes
@app.route("/category/add", methods=['POST'])
def add_item_category():
    """
    params: 
        add = name of category
        blacklisted = is the category blacklisted? boolean
        created_by = user_id object 
    """
    if request.method=='POST':
        category = request.args.get("category",None)
        blacklisted = request.args.get("blacklisted",None)
        blacklisted = (blacklisted=='True')
        created_by = request.args.get("created_by",None)
        try:
            Categories.add_item_category(category,blacklisted,created_by)
            return {"created": category}
        except:
            return {"failed": category}
    return jsonify("Bad Request")

@app.route("/category/edit", methods=['POST'])
def modify_item_category():
    '''
    Input: username(str), category(str), property(list), value(list)
    Func: Modify category
    Return: category(str)
    '''
    if request.method=='POST':
        category = request.args.get("category",None)
        property= request.args.get("property",None)
        value = request.args.get("value",None)
        if value=='True':
            value = 1
        if value=='False':
            value=0
        try:
            Categories.modify_item_category(category,property,value)
            return jsonify({category:"success"})
        except:
            return jsonify({category:"edit failed"})
    
    return jsonify("Bad Request")

@app.route("/category/delete", methods=['DELETE'])
def delete_item_category():
    '''
    Input: username(str), category(str)
    Func: Delete category
    Return: category(str)
    '''
    category = request.args.get('category',None)
    if request.method=='DELETE':
        try:
            Categories.remove_item_category(category)
            return {category: "deleted"}
        except:
            return {category: "failed"}
    else:
        return jsonify("Bad Request")

@app.route("/categories/getall", methods=["GET"])
def get_cats():
    categories = Categories.getall()
    print(categories, file=sys.stderr)
    return jsonify([cat[0] for cat in categories])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3307)
#
