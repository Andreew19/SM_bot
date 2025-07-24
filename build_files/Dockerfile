FROM ubuntu:22.04

WORKDIR /app
COPY requirements.txt bot.py alerts.py /app/

# Установка необходимого
RUN apt update && \
    apt install -y python3 python3-pip && \
    apt clean && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apt install nano -y && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["bash", "-c", "python3 bot.py & python3 alerts.py & wait"]

