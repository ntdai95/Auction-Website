docker compose up -d itemsdb transactionsdb usersdb watchlistdb messagesmongo messagesrabbitmq auctionsdb
#docker start itemsdb transactionsdb auctionsdb usersdb watchlistdb messagesmongo messagesrabbitmq
sleep 60
docker compose up items transactions users auctions watchlist frontend 

