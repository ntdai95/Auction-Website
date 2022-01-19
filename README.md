RUN Directions:

cd src/docker-setup
./runscript.sh
docker exec -it messagesrabbitmq bash
>> python3 message_rpc_server.py
