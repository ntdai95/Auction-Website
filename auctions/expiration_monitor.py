import time
import requests
import datetime


auctions_conf = {
    "host": "auctions",
    "port": 3318
}


while True:
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
    res = requests.get(f"http://{auctions_conf['host']}:{auctions_conf['port']}/auctions-to-close/{now}").json()
    for auction in res:
        requests.get(f"http://{auctions_conf['host']}:{auctions_conf['port']}/close-auction/{auction['auction_id']}")
        print(f"closed auction {auction['auction_id']}")

    time.sleep(60)
