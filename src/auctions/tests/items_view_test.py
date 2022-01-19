import requests

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
    "port": "3308"
}
transactions_conf={
    "host": "transactions",
    "port": "3305"
}


item_id="111_88"
res = requests.get(f'http://{auctions_conf["host"]}:{auctions_conf["port"]}/view-auction-by-id/{item_id}')
res=res.json()
print(res)