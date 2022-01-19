'''r

Implements Item and Category classes to act as object layer atop crud.py.
'''

# TODO add push in price to auctions service
# TODO add push in user watch list to users service

from dataclasses import dataclass
import datetime
import string
import random
import time
import crud
import os
import sys
message_client_path = os.path.join(os.path.dirname(__file__), '../../messages')
sys.path.append(message_client_path)
from message_rpc_client import MessageRpcClient

COUNTERFEIT_THRESHOLD = 5000

USERS = "http://users:3312/"

@dataclass
class Item:
    item_id: str = None
    name: str = None
    auction_id: str = None
    creation_date: str = None
    user_id: str = None
    description: str = None
    categories: list = None
    counterfeit: bool = False
    inappropriate: bool = False
    price: float = 1000000000
    sold: bool = False
    

    def __post_init__(self):
        """
            Generate an item id each time a new Item is initialized.
        """

        if self.item_id is None:
            self.item_id = self.generate_item_id()
            while not Item.check_unique_item_id(self.item_id):
                self.item_id = self.generate_item_id()

        self.creation_date=time.strftime('%Y-%m-%d %H:%M:%S', datetime.datetime.utcnow().timetuple())
            
    def batch_edit(self, keys=None, values=None):

        """
            Edits several properties at once.
        """
        if keys==None:
            props = vars(self)
            keys = list(props.keys())
            values = list(props.values())
            print(f"pre-fix {values}")
            values = [str(int(i)) if isinstance(i, (bool)) else i for i in values]
            print(f"post-fix {values}")
        crud.batch_update('items','item_id',self.item_id,keys,values)

        item_id = values[keys.index('item_id')] if 'item_id' in keys else self.item_id

        return Item.load(item_id)
    
    @staticmethod
    def remove_item(item_id):
        crud.delete('items','item_id',item_id)
        # TODO: INFORM WATCHLIST OF DELETION

    def list_item(self):
        #TODO
        raise NotImplementedError()

    def check_inappropriateness(self):
        '''
        Inappropriateness is a mapping from category to {True, False}.
        '''
        for each in self.categories.split(" | "):
            if Categories.blacklisted(each):
                client = MessageRpcClient()
                client.NotifyAdmins(self.item_id,'inappropriate')
                return True
        return False
   
    def remove_inappropriate_flag(self):
        self.inappropriate=False
        self.batch_edit(['inappropriate'],[False])
   
    def set_inappropriate_flag(self):
        self.counterfeit=True
        self.batch_edit(['inappropriate'],[True])
        client = MessageRpcClient()
        client.NotifyAdmins(self.item_id,'inappropriate')

    def remove_counterfeit_flag(self):
        self.counterfeit=False
        self.batch_edit(['counterfeit'],[False])
   
    def set_counterfeit_flag(self):
        self.counterfeit=True
        self.batch_edit(['counterfeit'],[True])
        client = MessageRpcClient()
        client.NotifyAdmins(self.item_id,'counterfeit')

    @staticmethod
    def view_flagged_items(field,user_id=None):
        if user_id:
            where = f"user_id = \'{user_id}\' AND {field}=TRUE"
        else:
            where = f"{field}= TRUE"
        flagged = \
        f"""
        SELECT item_id
        FROM items
        WHERE {where}
        """
        cursor = crud.conn.cursor()
        cursor.execute(flagged)
        items = cursor.fetchall()
        return tuple([i[0] for i in items])

    @staticmethod
    def search_for_item(params, values):
        get = crud.search('items','item_id',params, values)
        get = [i[0] for i in get]
        return get

    def edit_item_category(self, *, add=None, remove=None):
        '''Change item instance's category; function requires keyword arguments.'''
        categories = set(self.categories.split("|"))
        if add:
            categories.add(add)
        if remove:
            categories.remove(remove)

    @staticmethod
    def load(item_id):
        result = crud.read('items','item_id',item_id)[0]
        print(f"result item is {result}")
        return Item(*result)

    def write(self):
        crud.create('items',vars(self))

    @staticmethod
    def check_unique_item_id(item_id):
        unique = \
        f"""
        SELECT COUNT(1)
        FROM items
        WHERE item_id = \"{item_id}\";
        """
        cursor = crud.conn.cursor()
        cursor.execute(unique)
        return not bool(cursor.fetchone()[0])
    
    @staticmethod
    def generate_item_id():
        item_id = ''
        for i in range(25):
            item_id+=random.choice(string.digits+string.ascii_letters)
        return item_id
    
    def __str__(self):
        return str(vars(self))
    
        
class Categories:
    def __init__(self):
        pass

    @staticmethod
    def blacklisted(category):
        return bool(crud.read('categories','category',category,['blacklisted'])[0][0])

    @staticmethod
    def add_item_category(category,blacklisted=False,created_by=None):
        package = dict([('category',category),('created_by',created_by),('blacklisted',int(blacklisted))])
        crud.create('categories',package)

    @staticmethod
    def modify_item_category(category, property, value):
        crud.update('categories','category', category,property,value)
    
    @staticmethod
    def remove_item_category(category):
        crud.delete('categories','category',category)
    
    @staticmethod
    def fetch(category):
        """crud.read wrapper for category table;
        """
        fetched=crud.read('categories','category',category)
        return fetched[0]
    
    @staticmethod
    def getall():
        return crud.read('categories',1,1,['category'])

