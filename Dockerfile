FROM python:3.10-alpine

WORKDIR /opt/apps/discord-bot

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
