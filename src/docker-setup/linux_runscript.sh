docker build -f .\Dockerfile_App . --no-cache
docker build -f .\Dockerfile_MySQL . --no-cache
docker build -f .\Dockerfile_Mongo . --no-cache
docker build -f .\Dockerfile_RabbitMQ . --no-cache
docker-compose up -d itemsdb transactionsdb auctionsdb usersdb watchlistdb messagesmongo messagesrabbitmq
sleep 120
docker-compose up items transactions auctions users watchlist frontend
