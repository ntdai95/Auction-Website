docker-compose up -d itemsdb transactionsdb auctionsdb usersdb watchlistdb messagesmongo messagesrabbitmq
#docker start itemsdb transactionsdb auctionsdb usersdb watchlistdb messagesmongo messagesrabbitmq
sleep 120
docker-compose up items transactions auctions users watchlist frontend

