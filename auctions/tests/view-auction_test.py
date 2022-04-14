import requests
import pprint

# res= requests.get("http://localhost:5002/view-auction/4")
# print(res.json())

data={"id_ls":[7]}

res= requests.post("http://localhost:5002/view-auction",json=data)
pp=pprint.PrettyPrinter(indent=4)

pp.pprint(res.json())
