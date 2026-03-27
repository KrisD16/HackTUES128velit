from datetime import datetime
import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/", tz_aware=True)
db = client["hack_tues_12"]
statuses = db["statuses"]

class status:
    def __init__(self, user=None, path=None, created_at=None):
        self.user = user
        self.path = path
        self.created_at = datetime.now() if created_at is None else created_at

    def fromClassToMap(self):
        return {
            "user": self.user.fromClassToMap(),
            "path": self.path,
            "created_at": self.created_at
        }
    
    def fromMapToClass(self, hmap):
        self.user.fromMapToClass(hmap.get("user"))
        self.path = hmap.get("path")
        self.created_at = datetime.now() if hmap.get("created_at") is None else hmap.get("created_at")

    def addStatus(self):
        statuses.insert_one(self.fromClassToMap())