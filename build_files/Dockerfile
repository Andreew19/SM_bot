FROM ubuntu:22.04

WORKDIR /app
COPY requirements.txt bot.py alerts.py DB_config.py aggregateDB.py ini.sh  /app/

# Установка необходимого
RUN apt update && \
    apt install -y python3 python3-pip && \
    apt clean && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apt install nano -y && \
    apt -y install cron && \
    apt -y install sqlite3 && \
    chmod +x DB_config.py && \
    chmod +x aggregateDB.py &&\
    chmod +x ini.sh &&\
    mkdir db && \
    echo "* * * * * python3 /app/DB_config.py\n* * * * * python3 /app/aggregateDB.py" | crontab - &&\
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["bash", "-c", "bash ini.sh & python3 bot.py & python3 alerts.py &  cron -f & wait"]