import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/", tz_aware=True)
db = client["hack_tues_12"]
users = db["users"]
