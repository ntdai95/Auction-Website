from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from datetime import datetime
from flask_jsglue import JSGlue
import json
from decimal import Decimal

app = Flask(__name__)
jsglue = JSGlue(app)

items_conf = {
    "host": "items",
    "port": "3307"
}

users_conf = {
    "host": "users",
    "port": "3312"
}

auctions_conf = {
    "host": "auctions",
    "port": "3318"
}

transactions_conf = {
    "host": "transactions",
    "port": "3305"
}

watchlist_conf = {
    "host":"watchlist",
    "port": "3311"
}

item_ls = [
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

cart_ls = [
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

auction_ls = [
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
        if res is None:
            return redirect("/")

        if res["success"]:
            user_id=res["user_id"]
            isadmin = requests.get(f'http://{users_conf["host"]}:{users_conf["port"]}/admin/checkadmin',params={"user_id":user_id})
            isadmin = isadmin.json()["isAdmin"]
            isadmin = bool(isadmin)
            if isadmin:
                return redirect(url_for("admin_main", username=username,user_id=res["user_id"], admin=isadmin))
            else:
                return redirect(url_for("login_redirect", username=username,user_id=res["user_id"], admin=isadmin))
        else:
            return redirect('/')

@app.route('/login_redirect/<username>/<user_id>/<admin>', methods=["GET","POST"])
def login_redirect(username,user_id,admin):
    return render_template("users/loggedin.html", username=username, user_id=user_id, admin=admin)

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

        try:
            res = requests.post(f'http://{users_conf["host"]}:{users_conf["port"]}/user/create',params=data)
            if res.json()['user_id']:
                return redirect("/")
            else:
                return render_template("users/sign-up.html", error=True)
        except:    
            return render_template("users/sign-up.html", error=True)


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
    auction_res = requests.post(f"http://{auctions_conf['host']}:{auctions_conf['port']}/list-auctions-by-id",json={"item_id_ls":item_id_ls})
    if not auction_res:
        return render_template("items/myitems.html", item_ls=items)
    else:
        auction_res = auction_res.json()
        for item in items:
            if item["item_id"] in auction_res:
                item["auction_id"]=auction_res[item["item_id"]]

    return render_template("items/myitems.html", item_ls=items)

@app.route('/create-item',methods=["GET","POST"])
def create_item():
    if request.method == "GET":
        return render_template("items/createitem.html")
    elif request.method=="POST":
        data = request.form
        some_d ={
            "properties":[],
            "values":[]
        }

        for prop,val in data.items():
            some_d["properties"].append(prop)
            some_d["values"].append(val)

        res = requests.post(f"http://{items_conf['host']}:{items_conf['port']}/item/create",params=some_d)
        res=res.json()
        if res["created"]:
            return redirect(url_for('my_items', user_id=data["user_id"]))
        else:
            return redirect(url_for('create_item'))

@app.route('/item/<item_id>')
def item(item_id):
    res = requests.get(f'http://{items_conf["host"]}:{items_conf["port"]}/item/get/{item_id}')
    print(res.json())
    #TODO
    # res = requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/view-auction-by-id/{item_id}')
    #Check if there is an auction for the item
    #if not create an auction page button for it
    return render_template("items/item.html",item=item)

@app.route("/delete-item", defaults={"item_id":None} ,methods=["GET","POST"])
@app.route('/delete-item/<item_id>')
def delete_item(item_id):
    res = requests.delete(f'http://{items_conf["host"]}:{items_conf["port"]}/item/delete', params={'item_id':item_id})
    print(res.json())
    return "Deleted!"


###################################
# auction related
###################################


@app.route("/create-auction", defaults={"item_id":None} ,methods=["GET","POST"])
@app.route("/create-auction/<item_id>",methods=["GET","POST"])
def create_auction(item_id):
    if item_id:
        item_dict={
            "name": "item_placeholder_name",
            "picture": "",
            "item_id": item_id
        }
    else:
        item_dict={
            "name": "asdbajsd",
            "picture": "",
            "item_id": 1
        }

    if request.method=="POST":
        data = request.form.to_dict()
        res = requests.post(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/create-new-auction', json=data)     
        if not res:
            return render_template("auctions/createauction.html", item={})

        if res.json()["status"] == "success":
            return redirect(url_for('my_auctions', user_id=data["user_id"]))

    return render_template("auctions/createauction.html", item=item_dict)

@app.route("/my-auctions/<int:user_id>", methods=["GET"])
def my_auctions(user_id):
    res = requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/user-auctions/{user_id}')
    user_auction_ls = res.json()    
    user_auction_ls.sort(key=lambda x: datetime.strptime(x["auction_end"], "%a, %d %b %Y %H:%M:%S GMT"))
    
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        auction_id = request.form.get('auction_id')
        bid_price = request.form.get('bid_price')
        request.post(f"http://{auctions_conf['host']}:{auctions_conf['port']}/create-new-bid?user_id={user_id}&auction_id={auction_id}&bid_price={bid_price}")
    
    return render_template("auctions/myauctions.html", auction_ls=user_auction_ls)


@app.route('/active-auctions-redirect', methods=["GET"])
def active_redirect():
    return render_template("auctions/active-auctions-redirect.html")

@app.route('/active-auctions/<int:user_id>', methods=["GET"])
def view_participating_auctions(user_id):
    res= requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/view-active/{user_id}')
    try:
        user_auction_ls = res.json()["auctions"]
        return render_template("auctions/active-auctions.html", auction_ls=user_auction_ls)
    except:
        return render_template("auctions/active-auctions.html", auction_ls=[])


@app.route('/auction', defaults={"auction_id":None}, methods=["POST"])
@app.route('/auction/<int:auction_id>', methods=["GET","POST"])
def view_auction(auction_id):
    if request.method == "GET":
        res = requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/view-auction/{auction_id}').json()
        if res["highest_bids"]:
            res["curr_bid"] = res["highest_bids"]["bid_price"]

        return render_template("auctions/auction.html", item=res)
    elif request.method=="POST":
        data = request.form
        if "action" in data:
            if data["action"] == "close":
                auction_id = data["auction_id"]
                requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/get-winner/{auction_id}')

                data = {"item_id": res["item_id"], "user_id": res["winning_bid"][0]["user_id"]}
                requests.get(f'http://{transactions_conf["host"]}:{transactions_conf["port"]}/cart/addCart/{data["item_id"]}/{data["user_id"]}')

                close_data = {"auction_id": auction_id}
                requests.post(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/close-auction', json=close_data)
                requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/delete-auction/{auction_id}')
                return redirect(url_for("cart", user_id=res["winning_bid"][0]["user_id"]))

        requests.post(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/create-new-bid', json=data)
        return redirect(url_for("view_auction", auction_id=data["auction_id"]))
        
@app.route('/deleteauction/<auction_id>', methods=["DELETE"])
def deleteauction(auction_id):
    requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/delete-auction/{auction_id}')
        
@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("items/search.html", item_ls=[])
    elif request.method == "POST":
        search = request.form.get('search', None)
        if not search:
            return render_template("items/search.html", item_ls=[])

        if ";" in search:
            search = search.split(";")
        else:
            search = [search]

        params = []
        values = []
        for i in search:
            if ":" not in i:
                return jsonify('Bad Request')

            p, v = i.split(":")
            params.append(p)
            values.append(v)

        p = {'params': params, 'values': values}
        res = requests.get(f'http://{items_conf["host"]}:{items_conf["port"]}/items/search', params=p)
        if not res:
            return render_template("items/search.html", item_ls=[])

        items = res.json()['items']
        for item in items:
            item_id = item["item_id"]
            res = requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/view-auction-by-id/{item_id}').json()
            item["auction_info"] = res

    return render_template("items/search.html", item_ls=items)


@app.route('/settings', defaults={"user_id": None}, methods=["POST"])
@app.route('/settings/<user_id>', methods=["GET","POST"])
def settings(user_id):
    if request.method == "GET":
        return render_template("users/settings.html", user_id=user_id)
    elif request.method == "POST":
        username = ""
        data = request.form
        user_id = data["user_id"]
        user_info = {
            "user_id":data["user_id"]
        }

        if data["property"] == "password":
            user_info["password"] = data["password"]
            requests.post(f'http://{users_conf["host"]}:{users_conf["port"]}/user/update', params=user_info)
            return redirect(url_for('settings', user_id=user_id))
        elif data["property"] == "username":
            user_info["username"] = data["username"]
            username = data["username"]
            requests.post(f'http://{users_conf["host"]}:{users_conf["port"]}/user/update', params=user_info)
            return redirect(url_for('settings', user_id=user_id, username=username))
            
    return redirect(url_for('settings', user_id=user_id, username=username))

@app.route('/settings-name-direct/<username>/<user_id>')
def settings_name_redirect(username, user_id):
    return render_template("settings_name_redirect.html", username=username, user_id=user_id)

@app.route('/watchlist/<user_id>')
def watchlist(user_id):
    items = requests.get(f"http://watchlist:3311/watchlist/watching?user_id={user_id}")
    watchlist_ls = []
    for id in items:
        item = requests.get(f"http://items:3307/item/get?item_id={id}").json()['gotten']
        watchlist_ls.append(item)

    if request.method == 'POST':
        item_id = request.form.get("item_id")
        requests.get(f"http://watchlist:3311/watchlist/remove?user_id={user_id}&item_id={item_id}")

    return render_template("watchlist/watchlist.html", watchlist_ls=watchlist_ls)


###################################
# transaction related
###################################


@app.route('/cart/<user_id>')
@app.route('/cart')
def cart(user_id): 
    res = requests.get(f'http://{transactions_conf["host"]}:{transactions_conf["port"]}/cart/getCart_by_user?user_id={user_id}')
    item_list = []
    total = 0
    try:
        for each in res.json():
            id = each[0]
            item = requests.get(f'http://{items_conf["host"]}:{items_conf["port"]}/item/get/{id}') 
            item_list.append(item.json()['gotten'])
            total += Decimal(item.json()['gotten']['price'])

        return render_template("transactions/cart.html", cart_ls=item_list, total=total)
    except:
       return render_template("transactions/nullCart.html")


@app.route('/cart/delete/<item_id>/<user_id>')
@app.route('/cart/delete/')
def cart_delete(user_id, item_id): 
    requests.delete(f'http://{transactions_conf["host"]}:{transactions_conf["port"]}/cart/deleteCart/{item_id}/{user_id}')
    return cart(user_id)

@app.route('/order/<user_id>')
@app.route('/order')
def order(user_id): 
    res = requests.get(f'http://{transactions_conf["host"]}:{transactions_conf["port"]}/cart/getCart_by_user?user_id={user_id}').json()
    item_list = []
    total = 0
    try:
        for each in res:
            id = each[0]
            item = requests.get(f'http://{items_conf["host"]}:{items_conf["port"]}/item/get/{id}') 
            item_list.append(item.json()['gotten'])
            total += Decimal(item.json()['gotten']['price'])

        return render_template("transactions/order.html", cart_ls=item_list, total=total)
    except:
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
    res = requests.get(f'http://{transactions_conf["host"]}:{transactions_conf["port"]}/cart/getCart_by_user?user_id={user_id}').json()
    requests.post(f'http://{transactions_conf["host"]}:{transactions_conf["port"]}/cart/executeOrder?user_id={user_id}')
    try:
        for each in res:
            parameters = {'item_id': each[0], 'properties': 'sold','values': 1}
            requests.post(f'http://{items_conf["host"]}:{items_conf["port"]}/item/edit', params=parameters)
    except:
        pass

    return render_template("transactions/order_complete.html")

###################################
# admin related
###################################

@app.route('/admin', methods=['GET','POST'])
def admin_main():
    """
    DELETE AND SUSPEND USERS
    """
    delete = request.form.get('delete_user_id', None)
    suspend = request.form.get("suspend_user_id", None)
    if delete:
        requests.delete(f"http://users:3312/admin/deleteuser?user_id={delete}")

    if suspend:
        requests.post(f"http://users:3312/admin/suspenduser?user_id={suspend}")

    category = request.form.get('category2')
    if not category:
        category = request.form.get('category1')

    categories = requests.get("http://items:3307/categories/getall")
    if categories:
        categories=categories.json()

    if request.form.get("add"): 
        blacklisted = request.form.get('blacklisted')
        if blacklisted == 'on':
            blacklisted = True
        else:
            blacklisted = False

        requests.post(f"http://items:3307/category/add?category={category}&blacklisted={blacklisted}")

    if request.form.get('delete'):
        requests.delete(f"http://items:3307/category/delete?category={category}")

    if request.form.get("edit"):
        blacklisted = request.form.get('blacklisted')
        if blacklisted == 'on':
            blacklisted = True
        else:
            blacklisted = False

        requests.post(f"http://items:3307/category/edit?category={category}&value={blacklisted}&property=blacklisted")

    auctions_ls = []
    if request.form.get("see_auctions"):
        res= requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/admin-view-active')
        if not res:
            auction_ls = []
        else:
            auction_ls=res.json()            
            auction_ls.sort(key=lambda x:datetime.strptime(x["auction_end"], "%a, %d %b %Y %H:%M:%S GMT"))

        if not auctions_ls:
            return render_template("admin/adminauctions.html", auction_ls=auction_ls, auctions=True)

    return render_template("admin/admin.html", categories=categories, auctions_ls=auctions_ls)

@app.route("/admin/inappropriate_items")
def inapp():
    items = requests.get("http://items:3307/items/flagged?field=inappropriate")
    items_ls = []
    for i in items:
        a = requests.get(f"http://items:3307/item/get/{i}").json()
        try:
            if a:
                items_ls.append(a['gotten'])
        except:
            pass

    return render_template("admin/inapp.html", items_ls=items_ls)

@app.route("/admin/counterfeit_items")
def counter():
    items = requests.get("http://items:3307/items/flagged?field=counterfeit")
    items_ls = []
    for i in items:
        a = requests.get(f"http://items:3307/item/get/{i}").json()
        try:
            if a:
                items_ls.append(a['gotten'])
        except:
            pass

    return render_template("admin/counter.html", items_ls=items_ls)

@app.route('/admin/support_messages')
def admin_suport_messages():
    return render_template("admin_support_messages.html")
