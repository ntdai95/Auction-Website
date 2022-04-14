import unittest
import json
import random
import datetime
import requests

from app import app
class AuctionTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def create_auction(self):
        for i in range(20):
            payload={
                "auction_type":[random.choice("FB SB BN".split())],
                "start_date":datetime.datetime.now().strftime("%Y-%m-%d"),
                "start_time": f"{random.randrange(0,23)}:{random.randrange(0,60)}",
                "end_date":(datetime.datetime.now() + datetime.timedelta(days=random.randrange(1,5))).strftime("%Y-%m-%d"),
                "end_time": f"{random.randrange(0,23)}:{random.randrange(0,60)}",
                "item_id": random.randrange(100)
            }
            res = self.client().post('create-new-auction', data = payload)
            self.assertEqual(res.status_code, 201)

    # def delete_auction(self):
    #     pass
    # def edit_auction(self):
    #     pass
    # def create_bid(self):
    #     pass