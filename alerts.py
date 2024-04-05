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
    def get_cpu_load(): 
        return psutil.cpu_percent(interval=1) 

    cpu_load = get_cpu_load()

    if cpu_load > 0.3:
        url = f"https://api.telegram.org/bot{bot}/sendMessage?chat_id={chat_id}&text=Если Вы видите это сообщение, то подключение уведомдений прошло успешно✅ \n\n Пожалуйста дайте обратную связь: @Andrew_DS"
        requests.post(url)

while True:
    time.sleep(10)
    send_alerts()