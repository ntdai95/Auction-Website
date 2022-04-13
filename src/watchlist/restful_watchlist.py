import crud
import datetime
from flask import Flask, request
import os
import sys
message_client_path = os.path.join(os.path.dirname(__file__), '../messages')
sys.path.append(message_client_path)
from message_rpc_client import MessageRpcClient

app = Flask(__name__)
 
client = MessageRpcClient()
"""
    user wants to watch item
    we add (user, item) to watchlist
    change happens in item, and the watchlist is notified
    watchlist gets all watchers
    sends notification
"""

@app.route("/watchlist/add", methods=['POST','GET'])
def user_add_request():
    '''
    Input: item_id(int), change_type(int)
    Func: Update item's status and send notification
    # item statuses: price change, availability change
    Return: None
    '''
    user_id = request.args.get('user_id')
    item_id = request.args.get('item_id')
    crud.create('watchlist',{'user_id':user_id,'item_id':item_id, 'watchlist_id':str(user_id)+item_id})

@app.route("/watchlist/remove", methods=['POST','GET'])
def user_remove_request():
    '''
    Input: user_id (int), item_id(int)
    Func: Remove item to watchlist and send notification
    Return: None
    '''
    user_id = request.args.get('user_id')
    item_id = request.args.get('item_id')
    crud.delete('watchlist','watchlist_id',str(user_id)+item_id)

@app.route("/watchlist/process", methods=['POST','GET'])
def process_item_status_change(item_id,change_type,property=None, value=None):
    '''
    Input: user_id (int), item_id(int)
    Func: Reflect the change in price and availability of 
          an item to watchlist and send notification
    Return: None
    '''
    item_id = request.args.get('item_id')
    change_type = request.args.get('change_type')
    props = request.args.getlist('property')
    vals = request.args.getlist('value')

    # item statuses: price change, availability change
    users = crud.read('watchlist','item_id',item_id,columns=['user_id'])
    users = [(i[0],i[3]) for i in users]
    if users ==[]:
        return None

    if change_type==0:
        """ item is no longer available"""
        for user in users:
            client.SendingNotification(receiving_user_id=user[0], 
                                       item_id=item_id,
                                       notification_type="itemRemovalWatchlist")
            # search watchlist table for all users item_id
            # send notification to each user that we're removing them from the watch list b/c item is gone
            # delete from watch list
            crud.delete('watchlist', 'item_id', item_id)
        
    if change_type==1:
        #notify user of price change max once per per day? 
        for user in users:
            if (datetime.datetime(user[1]) - datetime.datetime.now()).seconds < 60*24*60:
                # TODO add a price into the sent message?
                client.SendingNotification(receiving_user_id=user[0],
                                           item_id=item_id,
                                           notification_type="itemPriceChangeWatchlist")
@app.route("/watchlist/watching", methods=['GET'])
def watching():
    user_id = request.args.get('user_id')
    items = crud.search('watchlist','item_id',['user_id'],[user_id])
    return items


if __name__ =="__main__":
    app.run(host="0.0.0.0", port=3311)
