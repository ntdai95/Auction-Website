from types import MethodDescriptorType
from flask import Flask, render_template, request, jsonify,redirect, url_for
import requests
from functools import wraps
# from flask_cors import CORS
from datetime import datetime, timedelta
from flask_jsglue import JSGlue
import json
from decimal import Decimal
import sys

import string
import random
# import mysql.connector # pip3 install mysql-connector
# import bcrypt
# import configparser
import io
import sys
from requests.api import get

from werkzeug.wrappers import ETagRequestMixin

# from auctions.app import do_query

app = Flask(__name__)
jsglue = JSGlue(app)

items_conf={
    "host": "items",
    "port": "3307"
}
users_conf={
    "host": "users",
    "port": "3312"
}
auctions_conf={
    "host": "auctions",
    "port": "3318"
}
transactions_conf={
    "host": "transactions",
    "port": "3305"
}

watchlist_conf={
    "host":"watchlist",
    "port": "3311"
}


chats = {
     "abcde": {
         "authorized_users": {
             "as3215jhkg231hjgkl4123": {"username": "Alice", "expires": "2020-02-15T20:53:15Z"},
            "session_token_12": {"username": "bob", "expires": "2020-02-15T20:57:22Z"}
         },
         "magic_key": "some_really_long_key_value",
         "messages": [
            {"username": "Alice", "body": "Hi Bob!"},
            {"username": "Bob", "body": "Hi Alice!"},             {"username": "Alice", "body": "Knock knock"},
             {"username": "Bob", "body": "Who's there?"},
         ]
    },
    "pokop": {
         "authorized_users": {
             "as3215jhkg231hjgkl4123": {"username": "Alice", "expires": "2020-02-15T20:53:15Z"},
            "session_token_12": {"username": "bob", "expires": "2020-02-15T20:57:22Z"}
         },
         "magic_key": "another_long_string",
         "messages": [
            {"username": "Alice", "body": "Hi Bob!"},
            {"username": "Bob", "body": "Hi Alice!"},             {"username": "Alice", "body": "Knock knock"},
             {"username": "Bob", "body": "Who's there?"},
         ]
    }
 }

user = {
    "id":"AbeLincoln22",
    "emailaddress":"abe@lincoln.com",
    "admin": False,
    }


item_ls=[
     {
         "name":"gba",
         "id":"asd",
         "description":"the gameboy color mint condition",
         "price":"$50",
         "current_bid":"$85",
         "auction_start_time":"yesterday",
         "action_end_time":"tomorrow",
         "status":"on",
         "auction_html":"http://www.google.com",
         "item_id":99
     },
     {
         "name":"gba",
         "id":"QWE",
         "description":"the gameboy color mint condition",
         "price":"$50",
         "current_bid":"$85",
         "auction_start_time":"yesterday",
         "action_end_time":"tomorrow",
         "status":"on",
         "auction_html":"https://www.google.com",
         "item_id":45
     },
     {
         "name":"gba",
         "id":"123",
         "description":"the gameboy color mint condition",
         "price":"$50",
         "current_bid":"$85",
         "auction_start_time":"yesterday",
         "action_end_time":"tomorrow",
         "status":"on",
         "auction_html":"https://www.google.com",
         "item_id":3
     }
 ]

cart_ls=[
     {
         "name":"my soul",
         "link":"www.google.com",
         "sold_price":"$1.00"
     },
     {
         "name":"my cat",
         "link":"www.google.com",
         "sold_price":"$10.00"
     }
 ]

auction_ls=[
     {
         "name":"cat",
         "description":"the gameboy color mint condition",
         "price":"$50",
         "current_bid":"$85",
         "auction_start_time":"yesterday",
         "action_end_time":"tomorrow",
         "status":"on",
         "auction_html":"http://www.google.com"
     },
     {
         "name":"dog",
         "description":"the gameboy color mint condition",
         "price":"$50",
         "current_bid":"$85",
         "auction_start_time":"yesterday",
         "action_end_time":"tomorrow",
         "status":"on",
         "auction_html":"https://www.google.com"
     },
     {
         "name":"gerbil",
         "description":"the gameboy color mint condition",
         "price":"$50",
         "current_bid":"$85",
         "auction_start_time":"yesterday",
         "action_end_time":"tomorrow",
         "status":"on",
         "auction_html":"https://www.google.com"
     }
 ]

dumb_cat=[
     {"name":"books",
     "id":"123"},
     {"name":"toys",
     "id":"321"},
     {"name":"cars",
     "id":"abc"}
 ]

###################################
# user related
###################################

@app.route('/', methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template('index.html')
    elif request.method=="POST":
        username = request.form.get('username',None)
        password = request.form.get('password',None)
        data = {'username':username,'password':password}

        res = requests.get(f'http://{users_conf["host"]}:{users_conf["port"]}/user/login',params=data)
        res=res.json()
        print(res)
        if res is None:
            return redirect("/")
        if res["success"]:
            user_id=res["user_id"]
            isadmin = requests.get(f'http://{users_conf["host"]}:{users_conf["port"]}/admin/checkadmin',params={"user_id":user_id})
            isadmin = isadmin.json()["isAdmin"]
            isadmin = bool(isadmin)
            print(type(isadmin))
            print(isadmin)
            if isadmin:
                return redirect(url_for("admin_main",username=username,user_id=res["user_id"],admin=isadmin))
            else:
                return redirect(url_for("login_redirect",username=username,user_id=res["user_id"],admin=isadmin))
        else:
            return redirect('/')

@app.route('/login_redirect/<username>/<user_id>/<admin>', methods=["GET","POST"])
def login_redirect(username,user_id,admin):
    print(username, file=sys.stderr)
    print(user_id, file=sys.stderr)
    print(admin, file=sys.stderr)
    return render_template("users/loggedin.html",username=username,user_id=user_id,admin=admin)

@app.route('/user/<username>', methods=["GET","POST"])
def loggedin(username):
    pass

@app.route('/logout', methods=["GET","POST"])
def logout():
    return redirect('/')

@app.route('/sign-up', methods=["GET","POST"])
def sign_up():
    if request.method=="GET":
        return render_template("users/sign-up.html",error=False)
    elif request.method=="POST":
        username = request.form.get('username',None)
        password = request.form.get('password',None)
        email = request.form.get('email',None)
        data = {'username':username,'password':password,'email':email}
        print(f"[DATA RECEIVED] {data}")
        try:
            res = requests.post(f'http://{users_conf["host"]}:{users_conf["port"]}/user/create',params=data)
            if res.json()['user_id']:
                return redirect("/")
            else:
                return render_template("users/sign-up.html",error=True)
        except:    
            return render_template("users/sign-up.html",error=True)


###################################
# item specific
###################################

@app.route('/my-items/<user_id>')
def my_items(user_id):
    params = ['user_id']
    values = [user_id]
    p = json.dumps({'params': params, 'values': values})
    p = {'user_id': user_id}
    res = requests.get(f"http://{items_conf['host']}:{items_conf['port']}/items/allitems",params=p)
    if res==None:
        return render_template("items/myitems.html", item_ls=[])
    items = res.json()['items']
    item_id_ls=[i["item_id"] for i in items]
    print("creating item_id_ls", file=sys.stderr)
    print(item_id_ls, file=sys.stderr)
    auction_res = requests.post(f"http://{auctions_conf['host']}:{auctions_conf['port']}/list-auctions-by-id",json={"item_id_ls":item_id_ls})
    print(auction_res, file=sys.stderr)
    if auction_res==None:
        return render_template("items/myitems.html",item_ls=items)
    else:
        auction_res = auction_res.json()
        print("auction_res", sys.stderr)
        print(auction_res, file=sys.stderr)
        for item in items:
            if item["item_id"] in auction_res:
                item["auction_id"]=auction_res[item["item_id"]]
    return render_template("items/myitems.html",item_ls=items)

@app.route('/create-item',methods=["GET","POST"])
def create_item():
    if request.method == "GET":
        return render_template("items/createitem.html")
    elif request.method=="POST":
        data = request.form
        print(data)
        some_d ={
            "properties":[],
            "values":[]
        }
        for prop,val in data.items():
            some_d["properties"].append(prop)
            some_d["values"].append(val)
        res = requests.post(f"http://{items_conf['host']}:{items_conf['port']}/item/create",params=some_d)
        res=res.json()
        print("item createion results")
        print(res)
        if res["created"]:
            return redirect(url_for('my_items',user_id=data["user_id"]))
        else:
            return redirect(url_for('create_item'))

@app.route('/item/<item_id>')
def item(item_id):
    print(f"item_id recevied: {item_id}")
    res = requests.get(f'http://{items_conf["host"]}:{items_conf["port"]}/item/get/{item_id}')
    print(res.json())
    print("end of res")
    #TODO
    # res = requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/view-auction-by-id/{item_id}')
    #Check if there is an auction for the item
    #if not create an auction page button for it
    return render_template("items/item.html",item=item)

@app.route("/delete-item", defaults={"item_id":None} ,methods=["GET","POST"])
@app.route('/delete-item/<item_id>')
def delete_item(item_id):
    #item_id = requests.args.get('item_id')
    print(f"delete item_id recevied: {item_id}")
    res = requests.delete(f'http://{items_conf["host"]}:{items_conf["port"]}/item/delete',
                                 params={'item_id':item_id})
    print(res.json())
    return ("Deleted!")

###################################
# auction related
###################################

@app.route("/create-auction", defaults={"item_id":None} ,methods=["GET","POST"])
@app.route("/create-auction/<item_id>",methods=["GET","POST"])
def create_auction(item_id):
    if item_id:
        #search item datebase for details
        item_dict={
            "name":"item_placeholder_name",
        "picture":"",
        "item_id":item_id
        }
    else:
        item_dict={"name":"asdbajsd",
        "picture":"",
        "item_id":1}
    if request.method=="POST":
        data=request.form.to_dict()
        print(data)
        res = requests.post(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/create-new-auction',json=data)     
        if res is None:
            return render_template("auctions/createauction.html",item = {})
        if res.json()["status"]=="success":
            return redirect(url_for('my_auctions',user_id=data["user_id"]))
    return render_template("auctions/createauction.html",item = item_dict)

@app.route("/my-auctions/<int:user_id>", methods=["GET"])
def my_auctions(user_id):
    print("received my-auctions page")
    res= requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/user-auctions/{user_id}')
    user_auction_ls=res.json()    
    user_auction_ls.sort(key=lambda x:datetime.strptime(x["auction_end"],"%a, %d %b %Y %H:%M:%S GMT"))
    
    if request.method=='POST':
        user_id = request.form.get('user_id')
        auction_id = request.form.get('auction_id')
        bid_price = request.form.get('bid_price')
        request.post(f"http://{auctions_conf['host']}:{auctions_conf['port']}/create-new-bid?user_id={user_id}&auction_id={auction_id}&bid_price={bid_price}")
    return render_template("auctions/myauctions.html",auction_ls=user_auction_ls)


@app.route('/active-auctions-redirect',methods=["GET"])
def active_redirect():
    return render_template("auctions/active-auctions-redirect.html")

@app.route('/active-auctions/<int:user_id>',methods=["GET"])
def view_participating_auctions(user_id):
    res= requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/view-active/{user_id}')
    try:
        user_auction_ls=res.json()["auctions"]
        print("Finally",file= sys.stderr)
        print(user_auction_ls,file= sys.stderr)
        return render_template("auctions/active-auctions.html",auction_ls=user_auction_ls)
    except:
        return render_template("auctions/active-auctions.html",auction_ls=[])


@app.route('/auction',defaults={"auction_id":None},methods=["POST"])
@app.route('/auction/<int:auction_id>',methods=["GET","POST"])
def view_auction(auction_id):
    if request.method=="GET":
        res= requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/view-auction/{auction_id}')
        res =res.json()
        print(res)
        if res["highest_bids"]:
            res["curr_bid"]=res["highest_bids"]["bid_price"]
        return render_template("auctions/auction.html",item=res)
    elif request.method=="POST":
        data=request.form
        print(data)
        if "action" in data:
            if data["action"]=="close":
                print("GOT CLOSE",file=sys.stderr)
                print(data,file=sys.stderr)
                auction_id=data["auction_id"]
                res =requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/get-winner/{auction_id}')
                res=res.json()
                print(res,file=sys.stderr)
                data={}
                data["item_id"]=res["item_id"]
                bid=res["winning_bid"][0]
                data["user_id"]=bid["user_id"]
                # data["price"]=bid["bid_price"]
                print(data,file=sys.stderr)
                res = requests.get(f'http://{transactions_conf["host"]}:{transactions_conf["port"]}/cart/addCart/{data["item_id"]}/{data["user_id"]}')
                res=res.json()
                print(res,file=sys.stderr)
                close_data={"auction_id":auction_id}
                res =requests.post(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/close-auction',json=close_data)
                res =requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/delete-auction/{auction_id}')
                return redirect(url_for("cart",user_id=bid["user_id"]))
        res= requests.post(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/create-new-bid',json=data)
        res =res.json()
        print(res)
        return redirect(url_for("view_auction",auction_id=data["auction_id"]))
        
@app.route('/deleteauction/<auction_id>', methods=["DELETE"])
def deleteauction(auction_id):
    if request.method=="DELETE":
        res = requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/delete-auction/{auction_id}')
        res =res.json()
    return
        
@app.route('/search', methods=["GET","POST"])
def search():
    if request.method=="GET":
        return render_template("items/search.html",item_ls=[])
    elif request.method=="POST":
        search = request.form.get('search',None)
        if search is None:
            return render_template("items/search.html",item_ls=[])
        if ";" in search:
            search = search.split(";")
        else:
            search = [search]
        params = []
        values = []
        for i in search:
            if ":" not in i:
                return jsonify('Bad Request')
            p,v = i.split(":")
            params.append(p)
            values.append(v)
        print(f"{params} {values}")
        p = {'params': params, 'values': values}
        res = requests.get(f'http://{items_conf["host"]}:{items_conf["port"]}/items/search',params=p)
        if res is None:
            return render_template("items/search.html",item_ls=[])
        items = res.json()['items']
        for item in items:
            item_id =  item["item_id"]
            res = requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/view-auction-by-id/{item_id}')
            res=res.json()
            print(res)
            item["auction_info"]=res

    return render_template("items/search.html",item_ls=items)


#DAINGO PLEASE HELP ME GRAB INFORMATION FROM DB
@app.route('/settings', defaults={"user_id":None},methods=["POST"])
@app.route('/settings/<user_id>', methods=["GET","POST"])
def settings(user_id):
    # res=requests.get(f'http://{users_conf["host"]}:{users_conf["port"]}/user/info',
    #                  params={"user_id":user_id, 'username':True,'email':True,'user_rating':True})
    # res=res.json()
    # print(res,file=sys.stderr)
    # user={
    #     "user_id":user_id,
        
    # }
    # if res:
    if request.method=="GET":
        return render_template("users/settings.html",user_id=user_id)
    elif request.method=="POST":
        username = ""
        data=request.form
        user_id=data["user_id"]
        user_info={
            "user_id":data["user_id"]
        }
        if data["property"]=="password":
            user_info["password"]=data["password"]
            res=requests.post(f'http://{users_conf["host"]}:{users_conf["port"]}/user/update',
                     params=user_info)
            return redirect(url_for('settings',user_id=user_id))
        elif data["property"]=="username":
            user_info["username"]=data["username"]
            username==data["username"]
            res=requests.post(f'http://{users_conf["host"]}:{users_conf["port"]}/user/update',
                     params=user_info)
            # return redirect(url_for("settings_name_redirect",username=username,user_id=user_id))
            return redirect(url_for('settings',user_id=user_id,username=username))
            
    return redirect(url_for('settings',user_id=user_id,username=username))

@app.route('/settings-name-direct/<username>/<user_id>')
def settings_name_redirect(username,user_id):
    return render_template("settings_name_redirect.html",username=username,user_id=user_id)
@app.route('/watchlist/<user_id>')
def watchlist(user_id):
    items = requests.get(f"http://watchlist:3311/watchlist/watching?user_id={user_id}")
    watchlist_ls = []
    for id in items:
        item = requests.get("http://items:3307/item/get?item_id={id}").json()['gotten']
        watchlist_ls.append(item)
    if request.method=='POST':
        item_id = request.form.get("item_id")
        requests.get(f"http://watchlist:3311/watchlist/remove?user_id={user_id}&item_id={item_id}")
    return render_template("watchlist/watchlist.html",watchlist_ls=watchlist_ls)


###################################
# transaction related
###################################


@app.route('/cart/<user_id>')
@app.route('/cart')
def cart(user_id): 
    print("frontend_ cart page was called")
    res = requests.get(f'http://{transactions_conf["host"]}:{transactions_conf["port"]}/cart/getCart_by_user?user_id={user_id}')
    item_list = []
    total =0
    try:
        for each in res.json():
            id , price = each
            item = requests.get(f'http://{items_conf["host"]}:{items_conf["port"]}/item/get/{id}') 
            item_list.append(item.json()['gotten'])
            print(item.json(), file=sys.stderr)
            total += Decimal(item.json()['gotten']['price'])
            print(item.json()['gotten'])
            print(total)
            # item_list.append(item.json())
            # total += Decimal(item.json()['price'])
            print("Finally returning....")
            print(item_list)
        return render_template("transactions/cart.html",cart_ls=item_list, total = total)
    
    except:
       pass
       return render_template("transactions/nullCart.html")


@app.route('/cart/delete/<item_id>/<user_id>')
@app.route('/cart/delete/')
def cart_delete(user_id, item_id): 
    print("Reached", file=sys.stderr)
    res = requests.delete(f'http://{transactions_conf["host"]}:{transactions_conf["port"]}/cart/deleteCart/{item_id}/{user_id}')
    return cart(user_id)

@app.route('/order/<user_id>')
@app.route('/order')
def order(user_id): 
    res = requests.get(f'http://{transactions_conf["host"]}:{transactions_conf["port"]}/cart/getCart_by_user?user_id={user_id}')
    print(res.json())
    item_list = []
    total = 0
    try:
        for each in res.json():
            id , price = each
            item = requests.get(f'http://{items_conf["host"]}:{items_conf["port"]}/item/get/{id}') 
            item_list.append(item.json()['gotten'])
            total += Decimal(item.json()['gotten']['price'])
            # item_list.append(item.json())
            # total += Decimal(item.json()['price'])
            print("Order sums...")
            print(total)
        return render_template("transactions/order.html",cart_ls=item_list, total = total)
    except:
            #pass
        return render_template("transactions/nullCart.html")


@app.route('/ordercomplete/<user_id>')
@app.route('/ordercomplete')
def order_complete(user_id): 
    '''
    Takes: user_id (str)
    Func: Call Checkout 
            1. Get items in the cart
            2. Checkout in transaction microservice
            3. Mark items as sold in items microservice
    '''
    res = requests.get(f'http://{transactions_conf["host"]}:{transactions_conf["port"]}/cart/getCart_by_user?user_id={user_id}')
    payment = requests.post(f'http://{transactions_conf["host"]}:{transactions_conf["port"]}/cart/executeOrder?user_id={user_id}')
    print(payment,file=sys.stderr)
    try:
        for each in res.json():
            id , price = each
            parameters = {'item_id':id, 'properties':'sold','values':1}
            res2 = requests.post(f'http://{items_conf["host"]}:{items_conf["port"]}/item/edit', params=parameters)
    except:
        pass
    return render_template("transactions/order_complete.html")

###################################
# admin related
###################################

@app.route('/admin', methods=['GET','POST'])
def admin_main():
    
    """DELETE AND SUSPEND USERS"""
    delete = request.form.get('delete_user_id',None)

    suspend = request.form.get("suspend_user_id",None)
    
    print(f"suspend {suspend} delete {delete}", file=sys.stderr)
    if delete:
        requests.delete(f"http://users:3312/admin/deleteuser?user_id={delete}")
    if suspend:
        requests.post(f"http://users:3312/admin/suspenduser?user_id={suspend}")
    """------------------------------------------------------------------"""

    """ CATEGORY MANAGEMENT"""
    # add
    category = request.form.get('category2')
    if category:
        pass
    else:
        category = request.form.get('category1')
    categories = requests.get("http://items:3307/categories/getall")
    if categories:
        categories=categories.json()
    print(categories,file=sys.stderr)
    print(request.form.get('add'), file=sys.stderr)
    print(request.form.get('delete'), file=sys.stderr)
    if request.form.get("add"): 
        blacklisted = request.form.get('blacklisted')
        print(blacklisted, sys.stderr)
        if blacklisted=='on':
            blacklisted=True
        else:
            blacklisted = False
        requests.post(f"http://items:3307/category/add?category={category}&blacklisted={blacklisted}")
    # delete
    if request.form.get('delete'):
        requests.delete(f"http://items:3307/category/delete?category={category}")
    #edit
    if request.form.get("edit"):
        blacklisted = request.form.get('blacklisted')
        if blacklisted=='on':
            blacklisted=True
        else:
            blacklisted = False
        requests.post(f"http://items:3307/category/edit?category={category}&value={blacklisted}&property=blacklisted")
    auctions_ls = []
    if request.form.get("see_auctions"):
        res= requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/admin-view-active')
        if res is None:
            print(res, file=sys.stderr)
            auction_ls = []
        else:
            print(res, file=sys.stderr)
            auction_ls=res.json()
            
            auction_ls.sort(key=lambda x:datetime.strptime(x["auction_end"],"%a, %d %b %Y %H:%M:%S GMT"))
        auctions = False
        if auctions_ls:
            auctions = False
        else:
            auctions = True
            return render_template("admin/adminauctions.html",auction_ls=auction_ls, auctions=auctions)
    return render_template("admin/admin.html", categories=categories, auctions_ls = auctions_ls)

@app.route("/admin/inappropriate_items")
def inapp():
    items = requests.get("http://items:3307/items/flagged?field=inappropriate")
    items_ls = []
    for i in items:
        a = requests.get("http://items:3307/item/get/{i}").json()
        try:
            if a:
                a = a['gotten']
                items_ls.append(a)
        except:
            pass
    return render_template("admin/inapp.html", items_ls = items_ls)

@app.route("/admin/counterfeit_items")
def counter():
    items = requests.get("http://items:3307/items/flagged?field=counterfeit")
    items_ls = []
    for i in items:
        a = requests.get("http://items:3307/item/get/{i}").json()
        try:
            a = a['gotten']
            items_ls.append(a)
        except:
            pass
    return render_template("admin/counter.html", items_ls = items_ls)

@app.route('/admin/support_messages')
def admin_suport_messages():
    return render_template("admin_support_messages.html")

##################################
# misc 
###################################


"""
my-items will show items, it is the same page where an auctions are setup?
items will shows auctions information if any

item page show information on item and auction information

item-edit page fills in with current descriptions for editing with and make change button

active auctions are cards with acitive auctions user is participating in
bidding is done there

settings page where user settings are changed

"""

#TODO get admin close auction working
#TODO make create auction work with items
#TODO get expiration monitor working

#objectives integrate messaging
#integrate transaction
