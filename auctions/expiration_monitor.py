import requests
import datetime


auctions_conf = {
    "host": "auctions",
    "port": 3308
}


auctions_conf["host"]
while True:
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
    res= requests.get(f"http://{auctions_conf['host']}:{auctions_conf['port']}/auctions-to-close/{now}").json()
    for i in res:
        print(i)

    input("Press Enter to continue...")
