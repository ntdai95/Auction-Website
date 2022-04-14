import requests
import datetime
#view auctions every minute
#if auction finished send to cart
    #change auction_status to over
    #copy auction to finished table

auctions_conf={
    "host":"auctions",
    "port":3308
}
auctions_conf["host"]
while True:
    #find winner
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
    res= requests.get(f"http://{auctions_conf['host']}:{auctions_conf['port']}/auctions-to-close/{now}").json()
    for i in res:
        print(i)
        # res= requests.get(f"http://localhost:5002/close-auction/{now}").json()
        # send send order to transactions
        # res= requests.get(f"http://localhost:5002/transactions/add-to-cart/{now}").json()
    # res2= requests.get(f"http://localhost:5002/auctions-to-open/{now}").json()
    # print("auctions to start:")
    # for i in res2:
    #     print(i)
    #     res3 = requests.get(f"http://localhost:5002/open-auction/{i['auction_id']}").json()
    input("Press Enter to continue...")
    # time.sleep(10)#seconds