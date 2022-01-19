docker exec -it items bash -c "git pull"
docker stop items
docker start items

docker exec -it users bash -c "git pull"
docker stop users
docker start users

docker exec -it transaction bash -c "git pull"
docker stop transaction
docker start transaction


docker exec -it auctions bash -c "git pull"
docker stop auctions
docker start auctions


docker exec -it watchlist bash -c "git pull"
docker stop watchlist
docker start watchlist


docker exec -it frontend bash -c "git pull"
docker stop frontend
docker start frontend




