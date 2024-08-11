import pymongo 
import requests
import os
from datetime import timedelta, datetime

from dotenv import load_dotenv

load_dotenv()

bot = os.environ['TOKEN']
chat_id_user_one = os.environ['USER_1']
#chat_id_user_tow = os.environ['USER_2'] if have more users

chat_ids = [chat_id_user_one]

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


for doc in result:
      date = doc.get("_id")
      cpu_load_report = doc.get("cpu")
      Load_average_report = doc.get("load")
      memory_report = doc.get("memory")


      report_data = [f"CPU load percent: {cpu_load_report}", f"Load average: {Load_average_report}",f"Memory: {memory_report}"]
      process_report_data = "\n".join(report_data)



for chat_id in chat_ids:
    send_data_wrapper = f"✅ Report of: {date} \n\n {process_report_data}"
    get_report = f"https://api.telegram.org/bot{bot}/sendMessage?chat_id={chat_id}&text={send_data_wrapper}"
    requests.post(get_report)