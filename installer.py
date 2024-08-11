import os
import subprocess
from crontab import CronTab


#Устанавливаем все зависимости из requirements.txt

def install_requirements(requirements_file='requirements.txt'):
    try:
        subprocess.check_call(['pip', 'install', '-r', requirements_file])
        print(f"All dependencies from {requirements_file} have been installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing dependencies: {e}")
    except FileNotFoundError:
        print(f"The file {requirements_file} was not found.")

#Создаем файл .env (Даем пользователю ввести токен бота и базовый индентификатор пользователя)

token = input("Enter your bot token: ")
user_id = input("Enter user id: ")

env_vars = {
        "TOKEN": token,
        "USER_1": user_id
    }

def create_env_file(env_vars, filename='.env'):
    try:
        with open(filename, 'w') as env_file:
            for key, value in env_vars.items():
                env_file.write(f"{key}={value}\n")
        print(f"Environment variables have been written to {filename} successfully.")
    except Exception as e:
        print(f"An error occurred while creating the .env file: {e}")

#Устанавливаем mongoDB

def install_mongodb():
    commands = [
        "sudo apt-get install gnupg curl",
        "curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor",
        "echo \"deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse\" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list",
        "sudo apt-get update",
        "sudo apt-get install -y mongodb-org",
        "echo \"mongodb-org hold\" | sudo dpkg --set-selections",
        "echo \"mongodb-org-database hold\" | sudo dpkg --set-selections",
        "echo \"mongodb-org-server hold\" | sudo dpkg --set-selections",
        "echo \"mongodb-mongosh hold\" | sudo dpkg --set-selections",
        "echo \"mongodb-org-mongos hold\" | sudo dpkg --set-selections",
        "echo \"mongodb-org-tools hold\" | sudo dpkg --set-selections",
        "sudo service mongod start"
    ]
    
    for command in commands:
        subprocess.run(command, shell=True, check=True)
    
#Создание и ежеминутное обновление БД

def create_db():
    get_path_DB_config = os.path.abspath('DB_config.py')

    command_to_find = f'python3 {get_path_DB_config}'

    with CronTab(user='root') as cron:
        job_exists = any(job for job in cron if job.command == command_to_find)
        
        if job_exists:
            pass
        else:
            job = cron.new(command=command_to_find)
            job.minute.every(1)
            cron.write()

# ежедневный отчет о средней нагрузке

def day_report_load():

    get_path_aggregateDB = os.path.abspath('aggregateDB.py')

    command_to_find = f'python3 {get_path_aggregateDB}'

    with CronTab(user='root') as cron:
        job_exists = any(job for job in cron if job.command == command_to_find)

        if job_exists:
            pass
        else:
            job = cron.new(command=command_to_find)
            job.setall('0 18 * * *')
            cron.write()

            


#Создание отдельных screen сессий для запуска модулей бота (bot.py и alert.py)

def start_modules():
    subprocess.check_call(["screen", "-S", "start_bot", "python3", "bot.py"])
    subprocess.check_call(["screen", "-S", "start_alerts", "python3", "alerts.py"])

#Завершение программы установки

def final_install_programm():
    subprocess.check_call(['clear'])
    print("Программа установки успешно завершена!")

if __name__ == "__main__":
    install_requirements()
    create_env_file(env_vars)
    install_mongodb()
    create_db()
    day_report_load()
    start_modules()
    final_install_programm()
