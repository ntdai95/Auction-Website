import requests
import sys

# items networks test
body={'category':"cards", 'blacklisted': False, "created_by": 1 }
# res = requests.post("http://172.17.0.4:5004/",json=body)
res = requests.post("http://localhost:5004/",json=body)
# res = requests.post("http://items_db:5000/",json=body)