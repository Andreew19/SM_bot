import sqlite3
import requests
import os
from datetime import timedelta, datetime

from dotenv import load_dotenv

load_dotenv()

bot = os.environ['TOKEN']
chat_id_users = os.getenv("USERS").split(",")

conn = sqlite3.connect("/app/db/smb.db")
cursor = conn.cursor()

today = datetime.utcnow().date().isoformat()


cursor.execute('''
    SELECT
        DATE(created_at) as day,
        AVG(CPU_load_percent) as cpu,
        AVG(Load_avg_1) as avg_1,
        AVG(Load_avg_2) as avg_2,
        AVG(Load_avg_3) as avg_3,
        AVG(Memory_load_percent) as mem
    FROM server_load
    WHERE date(created_at) = ?
    GROUP BY day
    ORDER BY day ASC
''', (today, ))

rows = cursor.fetchall()


for row in rows:
    day , cpu, avg_1, avg_2, avg_3, mem = row
    report_data = [
        f"CPU load percent: {cpu:.2f}%",
        f"Load average: {avg_1:.2f}, {avg_2:.2f}, {avg_3:.2f}",
        f"Memory: {mem:.2f}%"
    ]
    process_report_data = "\n".join(report_data)

    for chat_id in chat_id_users:
        send_data_wrapper = f"✅ Report of:{today} \n\n{process_report_data}"
        get_report = f"https://api.telegram.org/bot{bot}/sendMessage"
        requests.post(get_report, data={"chat_id": chat_id, "text": send_data_wrapper})



conn.close()