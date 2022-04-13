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
    # print("executing")
    try:
        cur.execute(query, vars)
    except pymysql.Error as e:
        print(f"From pymysql: {e}")
    # print("getting res")
    if res == "one":
        # print("res was one")
        res = cur.fetchone()
        print(res)
    elif res == "all":
        print("res was all")
        res = cur.fetchall()
        print(res)
    else:
        res = True
    # print("do_query has res")
    conn.commit()
    cur.close()
    conn.close()
    print(res)
    print(f"finished query:({query}{vars}")
    return res


@app.route("/create-new-bid", methods=["POST"])
def CreateNewBid():
    """validate information given and create new bid returning bid object"""
    data = request.get_json()
    print(data)
    try:
        res = do_query(
            "insert into bids values(default,%s,%s,%s, now())",
            [data["bid_price"], data["user_id"], data["auction_id"]],
            res=None,
            fact="dict")

        ############
        curr_highest = requests.get(
            f"http://auctions:3008/curr_highest?auction_id={data['auction_id']}"
        )
        if data['bid_price'] <= curr_highest:
            return jsonify({
                "status": "fail",
                "message": "Invalid Bid, too low!"
            })
        requests.post(
            f"http://watchlist:3311/watchlist/process?item_id={data['item_id']}&change_type=1&property=price&value={data['bid_price']}"
        )
        requests.post(
            f"http://items:3307/item/edit?item_id={data['item_id']}&properties=price&values={data['bid_price']}"
        )
        ############
    except:
        return jsonify({
            "status": "fail",
            "message": "error in insertion of bid"
        })
    print("1/2 queries finished")
    try:
        res2 = do_query(
            "Select user_id, bid_price from bids where auction_id=%s order by bid_price desc limit 1",
            [data["auction_id"]],
            res="one",
            fact="dict")
        res2["status"] = "success"
       # message.SendingNotification(data['user_id'], data['item_id'], "buyerBid", time=None, timeunit=None):
    except:
        return jsonify({
            "status": "fail",
            "message": "error in retrieval of bid"
        })
    print("request complete")
    return jsonify(res2)


@app.route("/create-new-auction", methods=["POST"])
def CreateNewAuction():
    '''
    Input: data(json)
    Func: Create new auction
    Return: status(str), auction_id(str)
    '''
    data = request.get_json()
    print(data, file=sys.stderr)
    _auction_type = data["auction_type"]
    _item_id = data["item_id"]
    _user_id = data["user_id"]
    _auction_start = f"{data['start_date']} {data['start_time']}:00"
    _auction_end = f"{data['end_date']} {data['end_time']}:00"

    if datetime.datetime.strptime(
            data['start_date'] + " " + data['start_time'],
            '%Y-%m-%d %H:%M') < datetime.datetime.now():
        _auction_status = "on"
    else:
        _auction_status = "notst"
    print("formatted variables attempting query", file=sys.stderr)
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
            do_query("delete from auctions where auction_id=(%s)",
                     (request.form[auction_id]))
        except:
            print("An error occured")

    for i in res2:
        pass


@app.route("/user-auctions/<int:user_id>")
def get_user_auctions(user_id):
    '''
    Input: user_id(json)
    Func: Get all auctions of the user
    Return: res(list)
    '''
    res = do_query("select * from auctions where user_id=%s", [user_id],
                   res="all",
                   fact="dict")
    auction_ls = []
    # for i in res:
    #     auction_id=i["auction_id"]
    #     bid_res=do_query("select rank.* from (select *, row_number() over (partition by auction_id order by bid_price desc) from bids where auction_id=%s) rank where rank.row_number<3;",[auction_id],res="all",fact="dict")
    #     i[""]={"auction_details":auction_res,"bid_details":bid_res}
    #     print(f"got bid details for {auction_id}")
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
        "delete from auctions  where auction_id=%s",[auction_id])
    res["status"] = "success"
    return jsonify(res)


@app.route("/get-winner/<int:auction_id>", methods=["GET"])
def get_winner(auction_id):
    '''
    Input: auction_id(str)
    Func: Get winner of the auction
    Return: res(dict)
    '''
    print(auction_id)
    
    auction_res = do_query("select * from auctions where auction_id=%s",[auction_id],res="one",fact="dict")
    print(auction_res,file=sys.stderr)
    if auction_res["auction_type"]=="FB":
        bid_res=do_query("select * from bids where auction_id=%s order by bid_price desc limit 1",[auction_id],res="all",fact="dict")
    if auction_res["auction_type"]=="SB":
        bid_res=do_query("select * from bids where auction_id=%s order by bid_price desc limit 2",[auction_id],res="all",fact="dict")
        # if len(bid_res)==2:
        #     bid_res=bid_res[-1] 
    # if auction_res["auction_type"]=="BN":
    #     bid_res=do_query("select rank.* from (select *, row_number() over (partition by auction_id order by bid_price desc) from bids where auction_id=%s) rank where rank.row_number=2;",[auction_id],res="one",fact="dict")
    auction_res["winning_bid"]=[bid_res[-1]]
    auction_res["status"]="success"
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
                "select * from auctions where auction_id=%s", [auction_id],
                res="one",
                fact="dict")
            print("got auction details")

            bid_res = do_query(
                "Select user_id, bid_price from bids where auction_id=%s order by bid_price desc limit 1",
                (auction_id),
                res="one",
                fact="dict")
            if bid_res:
                print("got bid details")
            else:
                print("bid_res is empty")

        # for auction_id in id_ls:
        # auction_res = do_query("select * from auctions where auction_id=%s",[auction_id],res="all",fact="dict")
        # print("got auction details for {auction_id}")
        # if auction_res==None:
        #     res[auction_id]={"auction_details": False }
        # else:
        #     bid_res=do_query("select rank.* from (select *, row_number() over (partition by auction_id order by bid_price desc) from bids where auction_id=%s) rank where rank.row_number<3;",[auction_id],res="all",fact="dict")
        #     res[auction_id]={"auction_details":auction_res,"bid_details":bid_res}
        #     print(f"got bid details for {auction_id}")
        #     # if auction_res["auction_type"]=="BN":
        #     #     bid_res=do_query("select rank.* from (select *, row_number() over (partition by auction_id order by bid_price desc) from bids where auction_id=%s) rank where rank.row_number=2;",[auction_id],res="one",fact="dict")
        except:
            return jsonify({
                "status": "fail",
                "message": "Error in processing winner."
            })
        res = {"highest_bids": bid_res, **auction_res}
        res["status"] = "success"

        return jsonify(res)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3308, debug=True)


@app.route("/view-auction", methods=["POST"])
def view_auctions():
    print("post received")
    id_ls = request.get_json()["id_ls"]
    print(id_ls)
    res = {}
    # for each id check whether there is an auction for is
    for auction_id in id_ls:
        auction_res = do_query("select * from auctions where auction_id=%s",
                               [auction_id],
                               res="all",
                               fact="dict")
        print("got auction details for {auction_id}")
        if auction_res == None:
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
            print(f"got bid details for {auction_id}")
    # if auction_res["auction_type"]=="BN":
    #     bid_res=do_query("select rank.* from (select *, row_number() over (partition by auction_id order by bid_price desc) from bids where auction_id=%s) rank where rank.row_number=2;",[auction_id],res="one",fact="dict")
    res["status"] = "success"
    return jsonify(res)
    # except:
    #     return jsonify({"status":"fail", "message":"Error in processing winner."}), 500


@app.route("/change-auction", methods=["POST"])
def change_auction():
    '''
    Input: auction_id(str)
    Func: Edit the auction
    Return: status(str)
    '''
    print("post received")
    data = request.get_json()
    if not data["auction_id"]:
        return jsonify({"staus": "error", "message": "no auction_id"})
    print(data)
    try:
        _auction_id = data["auction_id"]
        _auction_type = data["auction_type"]
        _auction_start = f"{data['start_date']} {data['start_time']}:00"
        _auction_end = f"{data['end_date']} {data['end_time']}:00"
    except:
        print("error in received variables")
        return jsonify({
            "status": "fail",
            "message": "not all form variables were returned."
        })
    res = do_query(
        "UPDATE auctions SET auction_type = %s,auction_start = %s, auction_end= %s WHERE auction_id=%s",
        (_auction_type, _auction_start, _auction_end, _auction_id))
    res = {}
    res["status"] = "success"
    return jsonify(res)


@app.route("/view-auction-by-id/<item_id>", methods=["GET"])
def view_auction_by_item_id(item_id):
    '''
    Input: item_id(str)
    Func: View auction and bid for the item
    Return: res(dict)
    '''
    print('view auction by id is called with',file=sys.stderr)
    print(item_id,file=sys.stderr)
    try:
        auction_res = do_query("select * from auctions where item_id=%s",
                               [item_id],
                               res="one",
                               fact="dict")
        print("got auction details",file=sys.stderr)
    except:
        print("issue receiving auction details",file=sys.stderr)
        return jsonify({
            "status": "fail",
            "message": "issue receiving auction details"
        })
    print(auction_res,file=sys.stderr)
    if not auction_res:
        return jsonify({"status":"success", "auction_id":None})
    auction_id = auction_res["auction_id"]
    print(auction_id,file=sys.stderr)
    bid_res = do_query(
        "with ranks as (select *, row_number() over (partition by auction_id order by bid_price desc)  as 'rank' from bids) select * from ranks where auction_id=%s and ranks.rank<=3;",
        [auction_id],
        res="all",
        fact="dict")
    print(bid_res,file=sys.stderr)
    print("got bid details")
    print("issue receiving auction details")
    bid_res = {}
    # return jsonify({"status":"fail", "message":"issue receiving auction details"})
    # if auction_res["auction_type"]=="BN":
    #     bid_res=do_query("select rank.* from (select *, row_number() over (partition by auction_id order by bid_price desc) from bids where auction_id=%s) rank where rank.row_number=2;",[auction_id],res="one",fact="dict")
    res = {"highest_bids": bid_res, **auction_res}
    print("merged")
    res["status"] = "success"
    print("status updated")
    print(res,file=sys.stderr)
    return jsonify(res)


@app.route("/view-active/<int:user_id>", methods=["GET"])
def view_active(user_id):
    '''
    Input: user_id(str)
    Func: View only active auction for the user
    Return: auctions(dict), status(str)
    '''
    print(f"received {user_id}",file=sys.stderr)
    res = do_query("select distinct auction_id from bids where user_id=%s",
                   (user_id),
                   res="all",
                   fact="dict")
    # res = res
    print(res,file=sys.stderr)
    auction_id_ls = [i["auction_id"] for i in res]
    print(f"auction_id_ls: {auction_id_ls}",file=sys.stderr)
    if auction_id_ls:
        print("fetching auctions",file=sys.stderr)
        stmt = "select * from auctions where auction_id in ("
        cond = ",".join(auction_id_ls)
        stmt += cond + ")"
        print(stmt,file=sys.stderr)
        res2 = do_query(stmt, (), res="all", fact="dict")
        print(res2,file=sys.stderr)
        end_res = {"auctions": res2, "status": "success"}
        print(end_res,file=sys.stderr)
        return jsonify(end_res)
    else:
        end_res = {"auctions": [], "status": "success"}
        return jsonify(end_res,file=sys.stderr)

@app.route("/admin-view-active", methods=["GET"])
def admin_view_active():
    '''
    Input: 
    Func: View only active auction for all users
    Return: auctions(dict), status(str)
    '''
    res = do_query("select * from auctions WHERE auction_end > CURRENT_TIMESTAMP()", [],
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
        print("received")
        data = request.get_json()
        ls = data["item_id_ls"]
        print(ls)
        res = {}
        for i in ls:
            auction_res = do_query("select * from auctions where item_id=%s",
                                   i,
                                   res="one",
                                   fact="dict")
            res[i] = auction_res
        print(res)
        return jsonify(res)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3308, debug=True)

# TODO
# create newbid                 (done)
# create newauction             (done)
# create closeauction           (done)
# create editauction
# create viewauction            (needs testing)
