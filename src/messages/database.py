import pymongo
import pymongo.errors
from models import Message
from bson.json_util import dumps

USR = "messagesMongo"
PWD = "messagesMongo"

class MessageDB:
    def __init__(self) -> None:
        self.connection = pymongo.MongoClient(f'mongodb://{USR}:{PWD}@messagesMongo:27017') #3313
        self.db = self.connection['message_db']
        self.create_collections()
        self.message_collection = self.db.get_collection("message")


    def create_collections(self):
        try:
            self.db.create_collection("message")
            self.message_collection = self.db.get_collection("message")
            self.message_collection.insert_one({"message_id": 0, "sending_user_id": None, "message": "initial data"})
        except pymongo.errors.CollectionInvalid:
            pass


    ############################################
    #       MESSAGE COLLECTIONS QUERIES        #
    ############################################


    def create_message(self, message=Message):
        message_id = self.message_collection.find().sort("message_id", -1)[0]["message_id"] + 1
        message_attributes = message.dict()
        self.message_collection.insert_one({"message_id": message_id,
                                            "sending_user_id": message_attributes["sending_user_id"],
                                            "message": message_attributes["message"]})


    def read_message(self):
        messages = self.message_collection.find({"message_id": {"$gt": 0}})
        return dumps(messages)


    def delete_message(self, message=Message):
        message_attributes = message.dict()
        print(message_attributes)
        for k in message_attributes.keys():
            print(type(message_attributes[k]))
        self.message_collection.delete_one({"message_id": message_attributes["message_id"]})


if __name__ == "__main__":
    MessageDB()
