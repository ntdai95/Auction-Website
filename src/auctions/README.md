bidder updater


one database editor 

api for auction editing


setup docker for psql
connect form another docker
fill in api
release api v1


Auction_db 
run 
`mysql> source /auction_db_setup-sql`

Need to create api
-look at dai ngo's work



# setup information
Shall reserve port 3309 for auction_db
Shall reserve port 5002 for api endpoints

Therefore run api endpoints with command:
`flask run --port=5002`


DONT MAKE THIS DIFFICULT
-ACTIVE AUCTIONS IS A LIST OF AUCTIONS
-CLICK LINK TO AUCTION PAGE
-MAKE BIDS ON AUCTION PAGE 