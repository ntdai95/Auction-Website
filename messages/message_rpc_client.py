import pika
import uuid
import json
import requests


USERS = "http://users:3312"


class MessageRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='messagesrabbitmq'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)


    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    
    ############################################
    #            CUSTOMER SUPPORT              #
    ############################################


    def ViewIssueMessages(self, user_id):
        parameters = {"user_id": user_id}
        response = requests.get("http://users:3312/admin/checkadmin", params=parameters)
        if not response.json()["isAdmin"]:
            return {"success": False, "message": "Only admins are allowed to access all issue messages."}

        parameters = {"action": "ViewMessage"}
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(parameters))
        while self.response is None:
            self.connection.process_data_events()
        return json.loads(self.response)


    def SendIssueMessage(self, sending_user_id, message):
        parameters = {"action": "SendMessage",
                      "sending_user_id": sending_user_id,
                      "message": message}
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(parameters))
        while self.response is None:
            self.connection.process_data_events()
        return json.loads(self.response)


    def ReplyIssueMessage(self, message_id, message):
        parameters = {"action": "ReplyMessage",
                      "message_id": message_id,
                      "message": message}
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(parameters))
        while self.response is None:
            self.connection.process_data_events()
        return json.loads(self.response)

    
    ############################################
    #              NOTIFICATION                #
    ############################################


    def SendingNotification(self, receiving_user_id, item_id, notification_type, time=None, timeunit=None):
        parameters = {"action": "SendNotification",
                      "receiving_user_id": receiving_user_id,
                      "item_id": item_id,
                      "notification_type": notification_type,
                      "time": time,
                      "timeunit": timeunit}
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(parameters))
        while self.response is None:
            self.connection.process_data_events()
        return json.loads(self.response)
    
    def NotifyAdmins(self,item_id,notification_type):
        admins = requests.get(USERS+"/user/getalladmin").json()['admin_ids']
        print(f"[Notifyng Admins] {admins}")
        if admins:
            for admin in admins:
                self.SendingNotification(admin,item_id,notification_type)

if __name__ == "__main__":
    response = MessageRpcClient().SendIssueMessage(sending_user_id=2, message="lajdfjegje")
    print(f"SendIssueMessage: {response}")
    response = MessageRpcClient().ViewIssueMessages(user_id=2)
    print(f"ViewIssueMessages: {response}")
    response = MessageRpcClient().ReplyIssueMessage(message_id=1, message="replylnldfs")
    print(f"ReplyIssueMessage: {response}")
    response = MessageRpcClient().SendingNotification(receiving_user_id=2, item_id=3,
                                                      notification_type="watchlist",
                                                      time=None, timeunit=None)
    print(f"SendingNotification: {response}")
    response = MessageRpcClient().SendingNotification(receiving_user_id=2, item_id=3,
                                                      notification_type="sellerBid",
                                                      time=None, timeunit=None)
    print(f"SendingNotification: {response}")
    response = MessageRpcClient().SendingNotification(receiving_user_id=2, item_id=3,
                                                      notification_type="buyerBid",
                                                      time=None, timeunit=None)
    print(f"SendingNotification: {response}")
    response = MessageRpcClient().SendingNotification(receiving_user_id=2, item_id=3,
                                                      notification_type="biddingEnd",
                                                      time=4, timeunit="days")
    print(f"SendingNotification: {response}")

