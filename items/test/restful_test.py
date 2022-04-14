import requests
import json 
from random import randint

URL = "http://items:3307/"

created = requests.post(URL+"/item/create",data = {'empty':''})
print(created.text)

created = requests.post(URL+"/item/create",params= {'properties':['price','description'], 'values':[1000000,'something']})
print(created.url)
print(created.text)

get_item = json.loads(created.text)['created']
get = requests.get(URL+"/item/get", params={'item_id': get_item})
print(get.url)
print(get.text)
print(get_item)

edited = requests.post(URL+"/item/edit", params= {'item_id':get_item,'properties':['price','description'], 'values':[randint(0,100000000)/100.0,'something']})
print(edited.url)
print(edited.text)



