import requests

parameters = {"username": "DAI",
              "password": "admin"}

response = requests.post("http://users:3312/user/create", params=parameters)
print(response.json())


""" parameters = {"username": "DAVID",
              "password": "G4",
              "email": "nvjfbj@gmail.com"}

response = requests.post("http://users:3312/user/create", params=parameters)
print(response.json())
"""

# parameters = {"username": "DAVID",
#               "password": "G4"}

# response = requests.get("http://localhost:5000/user/login", params=parameters)
# print(response.json())

# parameters = {"username": "DAVID",
#               "password": "G5"}

# response = requests.get("http://localhost:5000/user/login", params=parameters)
# print(response.json())

# parameters = {"user_id": 1,
#               "username": "John",
#               "email": "newjohn@gmail.com"}

# response = requests.post("http://localhost:5000/user/update", params=parameters)
# print(response.json())

# parameters = {"user_id": 1}

# response = requests.delete("http://localhost:5000/user/delete", params=parameters)
# print(response.json())

# parameters = {"user_id": 100}

# response = requests.delete("http://localhost:5000/user/delete", params=parameters)
# print(response.json())

# parameters = {"user_id": 2}

# response = requests.post("http://localhost:5000/user/suspend", params=parameters)
# print(response.json())

# parameters = {"user_id": 100}

# response = requests.post("http://localhost:5000/user/suspend", params=parameters)
# print(response.json())

# parameters = {"username": "DAVID",
#               "password": "G4",
#               "email": "nvjfbj@gmail.com"}

# response = requests.get("http://localhost:5000/user/login", params=parameters)
# print(response.json())

# parameters = {"user_id": 2,
#               "user_rating": 4}

# response = requests.post("http://localhost:5000/user/rate", params=parameters)
# print(response.json())

# parameters = {"user_id": 2}

# response = requests.get("http://localhost:5000/admin/checkadmin", params=parameters)
# print(response.json())

# parameters = {"username": "Jesus",
#               "password": "admin"}

# response = requests.post("http://localhost:5000/user/create", params=parameters)
# print(response.json())

# parameters = {"user_id": 3}

# response = requests.get("http://localhost:5000/admin/checkadmin", params=parameters)
# print(response.json())

# parameters = {"user_id": 100}

# response = requests.get("http://localhost:5000/admin/checkadmin", params=parameters)
# print(response.json())

# parameters = {"username": "KAI",
#               "password": "admin"}

# response = requests.post("http://localhost:5000/user/create", params=parameters)
# print(response.json())


# parameters = {"username": "DAVID",
#               "password": "G4",
#               "email": "nvjfbj@gmail.com"}

# response = requests.post("http://localhost:5000/user/create", params=parameters)
# print(response.json())

# parameters = {"username": "GRAY",
#               "password": "GOOD",
#               "email": "olkjfi@gmail.com"}

# response = requests.post("http://localhost:5000/user/create", params=parameters)
# print(response.json())

# parameters = {"admin_id": 6,
#               "user_id": 4}

# response = requests.post("http://localhost:5000/admin/suspenduser", params=parameters)
# print(response.json())

# parameters = {"admin_id": 4,
#               "user_id": 6}

# response = requests.post("http://localhost:5000/admin/suspenduser", params=parameters)
# print(response.json())

# parameters = {"admin_id": 5,
#               "user_id": 4}

# response = requests.delete("http://localhost:5000/admin/deleteuser", params=parameters)
# print(response.json())

# parameters = {"admin_id": 4,
#               "user_id": 5}

# response = requests.delete("http://localhost:5000/admin/deleteuser", params=parameters)
# print(response.json())

# parameters = {"user_id": 2,
#               "username": True,
#               "email": True,
#               "user_rating": True,
#               "watchlist_parameter": True}

# response = requests.get("http://localhost:5000/user/info", params=parameters)
# print(response.json())

# parameters = {"user_id": 200,
#               "username": True,
#               "email": True,
#               "user_rating": True,
#               "watchlist_parameter": True}

# response = requests.get("http://localhost:5000/user/info", params=parameters)
# print(response.json())

# parameters = {"user_id": 2,
#               "item_id": 5}

# response = requests.post("http://localhost:5000/user/addwatchlist", params=parameters)
# print(response.json())

# parameters = {"user_id": 2,
#               "item_id": 35}

# response = requests.post("http://localhost:5000/user/addwatchlist", params=parameters)
# print(response.json())

# parameters = {"user_id": 2,
#               "item_id": 355}

# response = requests.post("http://localhost:5000/user/addwatchlist", params=parameters)
# print(response.json())

# parameters = {"user_id": 200,
#               "item_id": 5}

# response = requests.post("http://localhost:5000/user/addwatchlist", params=parameters)
# print(response.json())

# parameters = {"user_id": 2,
#               "item_id": 35}

# response = requests.delete("http://localhost:5000/user/removewatchlist", params=parameters)
# print(response.json())

# parameters = {"user_id": 200,
#               "item_id": 35}

# response = requests.delete("http://localhost:5000/user/removewatchlist", params=parameters)
# print(response.json())

# parameters = {"user_id": 2,
#               "item_id": 45}

# response = requests.delete("http://localhost:5000/user/removewatchlist", params=parameters)
# print(response.json())

# parameters = {"user_id": 2}

# response = requests.get("http://localhost:5000/user/getwatchlist", params=parameters)
# print(response.json())

# parameters = {"user_id": 200}

# response = requests.get("http://localhost:5000/user/getwatchlist", params=parameters)
# print(response.json())

# parameters = {"username": "DAI",
#               "password": "admin",
#               "email": "ngotandai95@gmail.com"}

# response = requests.post("http://localhost:5000/user/create", params=parameters)
# print(response.json())

# parameters = {"username": "DAI",
#               "password": "fjkdkjin",
#               "email": "ngotandai95@gmail.com"}

# response = requests.post("http://localhost:5000/user/create", params=parameters)
# print(response.json())
