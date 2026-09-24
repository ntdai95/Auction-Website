import requests

requests.post(
    "http://items:3307/category/add?category=XXXX&blacklisted=True&created_by=88"
)
requests.delete("http://items:3307/category/delete?category=XXXX")
