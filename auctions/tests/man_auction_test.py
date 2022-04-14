import unittest
import json
import random
import datetime
import requests

auction_id_ls=[]

def create_auction():
    for i in range(20):
        payload={
            "auction_type":[random.choice("FB SB BN".split())],
            "start_date":datetime.datetime.now().strftime("%Y-%m-%d"),
            "start_time": f"{random.randrange(0,23)}:{random.randrange(0,60)}",
            "end_date":(datetime.datetime.now() + datetime.timedelta(days=random.randrange(1,5))).strftime("%Y-%m-%d"),
            "end_time": f"{random.randrange(0,23)}:{random.randrange(0,60)}",
            "item_id": random.randrange(100)
        }
        res = requests.post('http://localhost:5002/create-new-auction', data = payload)
        assert res.status_code == 200
        auction_id_ls.append(res.get_json()["auction_id"])

def delete_auction():
    for i in auction_id_ls:
        payload={"auction_id":i}
        res = requests.post('http://localhost:5002/close-auction', data = payload)
        assert res.status_code == 200

def 
        
    # def delete_auction(self):
    #     pass
    # def edit_auction(self):
    #     pass
    # def create_bid(self):
    #     pass