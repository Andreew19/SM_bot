import requests
import os
import time
import psutil  

from dotenv import load_dotenv

load_dotenv()

bot = os.environ['TOKEN']
chat_id = os.environ['CHAT_ID']

print("Alerts up!")

def send_alerts():
    def is_disk_full(disk_usage):
        return disk_usage.percent >= 80

    disk_usage = psutil.disk_usage('/')
    if is_disk_full(disk_usage):
        message_hdd = f"https://api.telegram.org/bot{bot}/sendMessage?chat_id={chat_id}&text=❗ Внимание!  \n\n Диск заполнен на 80% или более 🚧 \n Необходимо освободить место!"
        requests.post(message_hdd)

    def get_cpu_load(): 
        return psutil.cpu_percent(interval=1) 

    cpu_load = get_cpu_load()

    if cpu_load > 0.3:
        message_cpu = f"https://api.telegram.org/bot{bot}/sendMessage?chat_id={chat_id}&text=❗ Внимание!  \n процессор загружен на {cpu_load}% 🔥"
        requests.post(message_cpu)

while True:
    time.sleep(10)
    send_alerts()