#!/usr/bin/env python3
import subprocess



def start_DB():
     subprocess.check_call(["sudo", "service", "mongod", "start"])


def screen_check(name):
    try:
        result = subprocess.run(['screen', '-list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if name in result.stdout:
            return True
        else:
            return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False

def start_module_bot():
    screen_name = "start_bot"
    exists = screen_check(screen_name)

    if exists:
        pass
    else:
        subprocess.check_call(["screen", "-S", "start_bot", "python3", "bot.py"])

def start_module_alert():
    screen_name = "start_alerts"
    exists = screen_check(screen_name)

    if exists:
        pass
    else:
        subprocess.check_call(["screen", "-S", "start_alerts", "python3", "alerts.py"])

def final_install_programm():
    subprocess.check_call(["clear"])
    print("Сервисы запущены")

if __name__ == "__main__":
    start_DB()
    start_module_bot()
    start_module_alert()
    final_install_programm()