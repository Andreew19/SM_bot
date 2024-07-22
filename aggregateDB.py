import pymongo 
from datetime import timedelta, datetime


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["SMB"]
server_load = db["server_load"]

date_28_days_ago = datetime.utcnow() - timedelta(days=28)


pipeline = [
    {
        "$match": {
            "create_at": {
                "$gte": date_28_days_ago
            }
        }
    },
    {
        "$project": {
            "day": {
                "$dateToString": {
                    "format": "%Y-%m-%d",
                    "date": "$create_at"
                }
            },
            "cpu": "$CPU_load_percent",
            "load": {
                "$arrayElemAt": ["$Load_verage", 2]
            },
            "mem": "$Memory_load_percent"
        }
    },
    {
        "$group": {
            "_id": "$day",
            "count": {
                "$sum": 1
            },
            "cpu": {
                "$avg": "$cpu"
            },
            "load": {
                "$avg": "$load"
            },
            "memory": {
                "$avg": "$mem"
            }
        }
    },
    {
        "$sort": {
            "_id": 1
        }
    }
]

result = server_load.aggregate(pipeline)
