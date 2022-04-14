import sys
sys.path.insert(1, '../core/')
# Add Fake Items
import datetime
from item import Item, Categories
from crud import *

# CLEAR CATEGORY TABLE BEFORE TEST 
conn.cursor().execute("DELETE FROM categories WHERE TRUE;");
conn.commit()

# Categories Testing
Categories.add_item_category('shoes',False,'kasyap')
Categories.add_item_category('obscenity',True,'kasyap')

print(f"shoes are not blacklisted: {Categories.blacklisted('shoes')}")
print(f"obscenity is blacklisted: {Categories.blacklisted('obscenity')}")

print('renaming obscenity to porn')
Categories.modify_item_category('obscenity','category','porn')
fetched = Categories.fetch('porn')
print(f"obscenity is now {fetched}")

# CLEAR ITEM TABLE BEFORE TEST 
conn.cursor().execute("DELETE FROM items WHERE TRUE;");
conn.commit()



#Item Testing
x = Item(
    item_id="abcd",
    auction_id="xkwjeud",
    photos="",
    creation_date=time.strftime('%Y-%m-%d %H:%M:%S', datetime.datetime.utcnow().timetuple()),
    user_id="kasyap",
    description= "shoes for men",
    categories= "",
    watched_by= "",
    flagged=False)

dte = "2021-22-07 23:00:01"

Item.creation_date = dte
# CREATE NEW ITEM RECORD
print("Item x looks like:")
print(x)
print("writing x to db")
x.write()

# LOAD ITEM
y = Item.load("abcd")
print(f"[LOADED ITEM] {y}")

# TODO: what if read returns several records? Can't b/c we're loading by items.PK.

# Edit Item
# need to test date edit, and string edit
y.batch_edit(['item_id','description','categories'],['munky','panda','porn | shoes'])
y = Item.load('munky')
print(f"[LOAD EDITED ITEM] {y}")

# Testing Item Id Uniqueness
print(f" UNIQUE ID: {Item.check_unique_item_id('munky')}")
print(f" UNIQUE ID: {Item.check_unique_item_id('huh')}")

#Create new Item
z = Item()
z.flagged=True
print(z)
z.write()
z_id = z.item_id
print(f"load written item {z_id}")
print(Item.load(z_id))
print(Item.view_flagged_items(z_id))
print(Item.view_flagged_items())
