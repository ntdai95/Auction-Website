from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import pymysql
import crud
import sys
import datetime

app = Flask(__name__)
CORS(app)

dbname = "auctions"
user = "auctions"
password = "auctions"
host = "auctionsdb"
port = 3328
db = "auctions"
auction_types_ls = ["first_bid", "second_bid", "buy_now"]
auction_status = ["on", "complete", "notst", "closed"]

def do_query(query, vars, res=None, fact=None):
    try:
        conn = pymysql.connect(host=host,
                               user=user,
                               password=password,
                               db=db,
                               port=port)
    except pymysql.Error as e:
        print(f"COULDNT EVEN CONNECT TO DB", file=sys.stderr)
        print(f"From pymysql: {e}", file=sys.stderr)

    if fact == "dict":
        try:
            cur = conn.cursor(pymysql.cursors.DictCursor)
        except pymysql.Error as e:
            print(f"From pymysql: {e}")
    else:
        try:
            cur = conn.cursor()
        except pymysql.Error as e:
            print(f"From pymysql: {e}")

    try:
        cur.execute(query, vars)
    except pymysql.Error as e:
        print(f"From pymysql: {e}")

    if res == "one":
        res = cur.fetchone()
    elif res == "all":
        res = cur.fetchall()
    else:
        res = True

    conn.commit()
    cur.close()
    conn.close()
    return res


@app.route("/create-new-bid", methods=["POST"])
def CreateNewBid():
    """validate information given and create new bid returning bid object"""
    data = request.get_json()

    try:
        do_query(
            "insert into bids values(default,%s,%s,%s, now())",
            [data["bid_price"],
            data["user_id"],
            data["auction_id"]],
            res=None,
            fact="dict")

        curr_highest = requests.get(f"http://auctions:3008/curr_highest?auction_id={data['auction_id']}")
        if data['bid_price'] <= curr_highest:
            return jsonify({"status": "fail", "message": "Invalid Bid, too low!"})

        requests.post(f"http://watchlist:3311/watchlist/process?item_id={data['item_id']}&change_type=1&property=price&value={data['bid_price']}")
        requests.post(f"http://items:3307/item/edit?item_id={data['item_id']}&properties=price&values={data['bid_price']}")
    except:
        return jsonify({"status": "fail", "message": "error in insertion of bid"})

    try:
        res2 = do_query(
            "Select user_id, bid_price from bids where auction_id=%s order by bid_price desc limit 1",
            [data["auction_id"]],
            res="one",
            fact="dict")

        res2["status"] = "success"
    except:
        return jsonify({"status": "fail", "message": "error in retrieval of bid"})

    return jsonify(res2)


@app.route("/create-new-auction", methods=["POST"])
def CreateNewAuction():
    '''
    Input: data(json)
    Func: Create new auction
    Return: status(str), auction_id(str)
    '''
    data = request.get_json()
    _auction_type = data["auction_type"]
    _item_id = data["item_id"]
    _user_id = data["user_id"]
    _auction_start = f"{data['start_date']} {data['start_time']}:00"
    _auction_end = f"{data['end_date']} {data['end_time']}:00"

    if datetime.datetime.strptime(data['start_date'] + " " + data['start_time'], '%Y-%m-%d %H:%M') < datetime.datetime.now():
        _auction_status = "on"
    else:
        _auction_status = "notst"

    auction = {
        'auction_type': _auction_type,
        "item_id": _item_id,
        "user_id": _user_id,
        "auction_status": _auction_status,
        "auction_start": _auction_start,
        "auction_end": _auction_end
    }

    res = crud.create('auctions', auction)
    return jsonify({"status": "success", 'auction_id': res})


@app.route("/curr-highest", methods=["POST"])
def curr_highest():
    '''
    Input: auction_id(json)
    Func: Get the current highest bid
    Return: status(str)
    '''
    if "auction_id" in request.get_json():
        res2 = do_query(
            "Select user_id, bid_price from bids where auction_id=%s order by bid_price desc limit 1",
            [request.get_json()["auction_id"]],
            res="one",
            fact="dict")

        res2["status"] = "success"
        return jsonify(res2)


@app.route("/close-auction", methods=["POST"])
def CloseAuction():
    '''
    Input: auction_id(json)
    Func: Close auction
    Return: status(str)
    '''
    if "auction_id" in request.get_json():
        try:
            do_query(
                "delete from auctions where auction_id=(%s)",
                (request.form['auction_id']))
        except:
            print("An error occured")


@app.route("/user-auctions/<int:user_id>")
def get_user_auctions(user_id):
    '''
    Input: user_id(json)
    Func: Get all auctions of the user
    Return: res(list)
    '''
    res = do_query(
        "select * from auctions where user_id=%s",
        [user_id],
        res="all",
        fact="dict")

    return jsonify(res)


@app.route("/auctions-to-close/<string:timestamp>", methods=["GET"])
def get_auctions_to_close(timestamp):
    '''
    Input: timestamp(time)
    Func: Close auction that reached time limit
    Return: res(dict)
    '''
    res = do_query(
        "select * from auctions where auction_status='on' and auction_end<(%s)",
        [timestamp],
        res="all",
        fact="dict")

    return jsonify(res)


@app.route("/auctions-to-open/<string:timestamp>", methods=["GET"])
def get_auctions_to_open(timestamp):
    '''
    Input: timestamp(time)
    Func: Open auction that reached the time
    Return: res(dict)
    '''
    res = do_query(
        "select * from auctions where auction_status='notst' and auction_start<to_timestamp(%s,'YYYY-MM-DD_HH:MI')",
        [timestamp],
        res="all",
        fact="dict")

    return jsonify(res)


@app.route("/open-auction/<int:auction_id>", methods=["GET"])
def open_auction(auction_id):
    '''
    Input: auction_id(str)
    Func: Open auction
    Return: res(dict)
    '''
    res = do_query(
        "update auctions set auction_status='on' where auction_id=%s returning auction_id, auction_status",
        [auction_id],
        res="one",
        fact="dict")

    res["status"] = "success"
    return jsonify(res)


@app.route("/close-auction/<int:auction_id>", methods=["GET"])
def close_auction(auction_id):
    '''
    Input: auction_id(str)
    Func: Close auction
    Return: res(dict)
    '''
    res = do_query(
        "update auctions set auction_status='on' where auction_id=%s returning auction_id, auction_status",
        [auction_id],
        res="one",
        fact="dict")

    res["status"] = "success"
    return jsonify(res)

@app.route("/delete-auction/<int:auction_id>", methods=["GET"])
def delete_auction(auction_id):
    '''
    Input: auction_id(str)
    Func: Close auction
    Return: res(dict)
    '''
    res = do_query(
        "delete from auctions  where auction_id=%s",
        [auction_id])

    res["status"] = "success"
    return jsonify(res)


@app.route("/get-winner/<int:auction_id>", methods=["GET"])
def get_winner(auction_id):
    '''
    Input: auction_id(str)
    Func: Get winner of the auction
    Return: res(dict)
    '''
    
    auction_res = do_query(
        "select * from auctions where auction_id=%s",
        [auction_id],
        res="one",
        fact="dict")
    
    if auction_res["auction_type"] == "FB":
        bid_res = do_query(
            "select * from bids where auction_id=%s order by bid_price desc limit 1",
            [auction_id],
            res="all",
            fact="dict")

    if auction_res["auction_type"] == "SB":
        bid_res = do_query(
            "select * from bids where auction_id=%s order by bid_price desc limit 2",
            [auction_id],
            res="all",
            fact="dict")
  
    auction_res["winning_bid"] = [bid_res[-1]]
    auction_res["status"] = "success"
    return jsonify(auction_res)

@app.route("/view-auction/<int:auction_id>", methods=["GET"])
def view_auction(auction_id):
    '''
    Input: auction_id(str)
    Func: Get info about the auction with the current highest bid
    Return: res(dict)
    '''
    if request.method == "GET":
        try:
            auction_res = do_query(
                "select * from auctions where auction_id=%s",
                [auction_id],
                res="one",
                fact="dict")

            bid_res = do_query(
                "Select user_id, bid_price from bids where auction_id=%s order by bid_price desc limit 1",
                (auction_id),
                res="one",
                fact="dict")
        except:
            return jsonify({"status": "fail", "message": "Error in processing winner."})

        res = {"highest_bids": bid_res, **auction_res}
        res["status"] = "success"
        return jsonify(res)

@app.route("/view-auction", methods=["POST"])
def view_auctions():
    id_ls = request.get_json()["id_ls"]
    res = {}
    for auction_id in id_ls:
        auction_res = do_query(
            "select * from auctions where auction_id=%s",
            [auction_id],
            res="all",
            fact="dict")

        if not auction_res:
            res[auction_id] = {"auction_details": False}
        else:
            bid_res = do_query(
                "select rank.* from (select *, row_number() over (partition by auction_id order by bid_price desc) from bids where auction_id=%s) rank where rank.row_number<3;",
                [auction_id],
                res="all",
                fact="dict")

            res[auction_id] = {
                "auction_details": auction_res,
                "bid_details": bid_res
            }
    
    res["status"] = "success"
    return jsonify(res)

@app.route("/change-auction", methods=["POST"])
def change_auction():
    '''
    Input: auction_id(str)
    Func: Edit the auction
    Return: status(str)
    '''
    data = request.get_json()
    if not data["auction_id"]:
        return jsonify({"staus": "error", "message": "no auction_id"})

    try:
        _auction_id = data["auction_id"]
        _auction_type = data["auction_type"]
        _auction_start = f"{data['start_date']} {data['start_time']}:00"
        _auction_end = f"{data['end_date']} {data['end_time']}:00"
    except:
        return jsonify({"status": "fail", "message": "not all form variables were returned."})

    do_query(
        "UPDATE auctions SET auction_type = %s,auction_start = %s, auction_end= %s WHERE auction_id=%s",
        (_auction_type, _auction_start, _auction_end, _auction_id))

    return jsonify({"status": "success"})


@app.route("/view-auction-by-id/<item_id>", methods=["GET"])
def view_auction_by_item_id(item_id):
    '''
    Input: item_id(str)
    Func: View auction and bid for the item
    Return: res(dict)
    '''
    try:
        auction_res = do_query(
            "select * from auctions where item_id=%s",
            [item_id],
            res="one",
            fact="dict")
    except:
        return jsonify({"status": "fail", "message": "issue receiving auction details"})

    if not auction_res:
        return jsonify({"status": "success", "auction_id": None})

    do_query(
        "with ranks as (select *, row_number() over (partition by auction_id order by bid_price desc)  as 'rank' from bids) select * from ranks where auction_id=%s and ranks.rank<=3;",
        [auction_res["auction_id"]],
        res="all",
        fact="dict")

    return jsonify({"highest_bids": {}, **auction_res, "status": "success"})


@app.route("/view-active/<int:user_id>", methods=["GET"])
def view_active(user_id):
    '''
    Input: user_id(str)
    Func: View only active auction for the user
    Return: auctions(dict), status(str)
    '''
    res = do_query(
        "select distinct auction_id from bids where user_id=%s",
        (user_id),
        res="all",
        fact="dict")

    auction_id_ls = [i["auction_id"] for i in res]
    if auction_id_ls:
        stmt = "select * from auctions where auction_id in (" + ",".join(auction_id_ls) + ")"
        res2 = do_query(stmt, (), res="all", fact="dict")
        return jsonify({"auctions": res2, "status": "success"})
    else:
        return jsonify({"auctions": [], "status": "success"})

@app.route("/admin-view-active", methods=["GET"])
def admin_view_active():
    '''
    Input: 
    Func: View only active auction for all users
    Return: auctions(dict), status(str)
    '''
    res = do_query(
        "select * from auctions WHERE auction_end > CURRENT_TIMESTAMP()",
        [],
        res="all",
        fact="dict")
    
    return jsonify(res)

@app.route("/list-auctions-by-id", methods=["POST"])
def list_auctions_by_item_id():
    '''
    Input: data(list)
    Func: List auctions for multiple items
    Return: res(dict)
    '''
    if request.method == "POST":
        data = request.get_json()
        ls = data["item_id_ls"]
        res = {}
        for i in ls:
            auction_res = do_query(
                "select * from auctions where item_id=%s",
                i,
                res="one",
                fact="dict")

            res[i] = auction_res

        return jsonify(res)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3308, debug=True)
