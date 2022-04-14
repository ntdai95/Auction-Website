import pika
import json
import smtplib
import requests
from database import MessageDB
from models import Message
from settings import EMAIL_ADDRESS, EMAIL_PASSWORD


class MessageRpcServer:
    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='messagesrabbitmq'))
        self.channel = self.connection.channel()
        self.run()


    def run(self):
        self.channel.queue_declare(queue='rpc_queue')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='rpc_queue', on_message_callback=self.on_request)
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()


    def on_request(self, ch, method, props, body):
        parameters = json.loads(body)
        if parameters["action"] == "ViewMessage":
            response = self.ViewIssueMessages()
        elif parameters["action"] == "SendMessage":
            response = self.SendIssueMessage(parameters)
        elif parameters["action"] == "ReplyMessage":
            response = self.ReplyIssueMessage(parameters)
        elif parameters["action"] == "SendNotification":
            response = self.SendingNotification(parameters)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=json.dumps(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)


    ############################################
    #            CUSTOMER SUPPORT              #
    ############################################


    def ViewIssueMessages(self):
        message = json.loads(MessageDB().read_message())
        response = {"success": True, "message": message}
        return response


    def SendIssueMessage(self, parameters):
        MessageDB().create_message(Message(sending_user_id=parameters["sending_user_id"],
                                           message=parameters["message"]))
        response = {"success": True, "message": "Issue message has been stored in the message database."}
        return response


    def ReplyIssueMessage(self, parameters):
        message = json.loads(MessageDB().read_message())
        selected_message_user_id = None
        for message_dict in message:
            if message_dict["message_id"] == parameters["message_id"]:
                selected_message_user_id = message_dict["sending_user_id"]
        
        user_info_parameters = {"user_id": selected_message_user_id,
                                "username": False, 
                                "email": True,
                                "user_rating": False,
                                "watchlist_parameter": False}
        response = requests.get("http://users:3312/user/info", params=user_info_parameters)
        email = response.json()["email"]
        if email:
            message = "Subject: {}\n\n{}".format("New response for your issue message!", parameters["message"])
            print(f"Your parameters are: {parameters}.")
            MessageDB().delete_message(Message(message_id=parameters["message_id"]))
            self.SendingEmail(email=email, message=message)
            response = {"success": True, "message": "An email with your response has been sent to the user's email address."}
        else:
            response = {"success": False, "message": "There is no user's email address found."}
        return response


    ############################################
    #              NOTIFICATION                #
    ############################################


    def SendingNotification(self, parameters):
        user_info_parameters = {"user_id": parameters["receiving_user_id"],
                                "username": False,
                                "email": True,
                                "user_rating": False,
                                "watchlist_parameter": False}
        response = requests.get("http://users:3312/user/info", params=user_info_parameters)
        email = response.json()
        if email:
            email = email["email"]
            if parameters["notification_type"] == "watchlist":
                subject = "New item is matching your watchlist criteria!"
                body = f"A new item with the item_id of {parameters['item_id']} has been found matching your watchlist criteria."
            elif parameters["notification_type"] == "itemRemovalWatchlist":
                subject = "Item removal from watchlist!"
                body = f"Your item with the item_id of {parameters['item_id']} has been removed from your watchlist."
            elif parameters["notification_type"] == "itemPriceChangeWatchlist":
                subject = "An item from watchlist has its price changed!"
                body = f"Your item with the item_id of {parameters['item_id']} has its price changed."
            elif parameters["notification_type"] == "sellerBid":
                subject = "New Bid on your listed bidding item!"
                body = f"Your listed bidding item with the item_id of {parameters['item_id']} has been bid on."
            elif parameters["notification_type"] == "buyerBid":
                subject = "Item has been outbid by another buyer!"
                body = f"Your bidding item with the item_id of {parameters['item_id']} has been out bid with a higher price by another buyer."
            elif parameters["notification_type"] == "biddingEnd":
                subject = "Item ends bidding soon!"
                body = f"The bidding item with the item_id of {parameters['item_id']} will end bidding in {parameters['time']} {parameters['timeunit']}."
            elif parameters["notification_type"] == "inappropriate":
                subject = "Item's category was inappropriate or it was flagged!"
                body = f"Item {parameters['item_id']} was flagged. Please review."
            elif parameters["notification_type"] == "counterfeit":
                subject = "Item's flagged as a counterfeit or it is a high value item that must be manually reviewd!"
                body = f"Item {parameters['item_id']} was flagged. Please review."


            message = "Subject: {}\n\n{}".format(subject, body)
            self.SendingEmail(email=email, message=message)
            response = {"success": True, "message": "The notification has been sent to the user's email address."}
        else:
            response = {"success": False, "message": "User with such user_id does not exists in the user database."}
        return response

    
    def SendingEmail(self, email, message):
        print(email)
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.ehlo()
            connection.starttls()
            connection.ehlo()
            connection.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            connection.sendmail(
                from_addr=EMAIL_ADDRESS,
                to_addrs=email,
                msg=message
            )
        

if __name__ == "__main__":
    MessageRpcServer()
