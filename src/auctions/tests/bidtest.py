import requests
import sys

host="auctions"


def diff_user(user=88,bid_price=100,auction=4):
    data={"auction_id":auction,"user_id":user,"bid_price":bid_price}
    res = requests.post(f"http://{host}:5002/create-new-bid",json=data)
    print(res.json())


if len(sys.argv)>1:
    if sys.argv[1]=="diff":
        diff_user(user=sys.argv[2],bid_price=sys.argv[3],auction=sys.argv[4])
else:
    data={"auction_id":4,"user_id":88,"bid_price":100.23}
    px_ls=[100,99,108,109,1]
    for i in px_ls:
        data["bid_price"]=i
        res = requests.post(f"http://{host}:3308/create-new-bid",json=data)
        print(res.json())