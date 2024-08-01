import requests
import os
import time
import psutil  
import atexit

from dotenv import load_dotenv

load_dotenv()

bot = os.environ['TOKEN']
chat_id_user_one = os.environ['USER_1']
chat_id_user_tow = os.environ['USER_2']

chat_ids = [chat_id_user_one, chat_id_user_tow]

print("Alerts up!")


def send_alerts():

    def is_disk_full(disk_usage):
        return disk_usage.percent >= 80

    disk_usage = psutil.disk_usage('/')
    

    def get_cpu_load(): 
        return psutil.cpu_percent(interval=1) 

    cpu_load = get_cpu_load()

    load_avg = psutil.getloadavg()

    cpu_count = psutil.cpu_count()

    mem_info = psutil.virtual_memory()

    for chat_id in chat_ids:
        if is_disk_full(disk_usage):
            message_hdd = f"https://api.telegram.org/bot{bot}/sendMessage?chat_id={chat_id}&text=❗ Внимание!  \n\n Диск заполнен на 80% или более 🚧 \n Пожалуйста, освободите место!"
            requests.post(message_hdd)
            print("Disk Alert")

        if load_avg[2] > cpu_count:
            message_cpu = f"https://api.telegram.org/bot{bot}/sendMessage?chat_id={chat_id}&text=❗ Внимание!  \n Превышена средняя загрузка процессора: {load_avg}🔥 \n текущая загрузка составляет: {cpu_load}%"
            requests.post(message_cpu)

        if mem_info.percent > 90:
            message_cpu = f"https://api.telegram.org/bot{bot}/sendMessage?chat_id={chat_id}&text=❗ Внимание!  \n ОЗУ заполнена на: {mem_info.percent}% ⚠"
            print("RAM alert")


while True:
    time.sleep(10)
    send_alerts()
