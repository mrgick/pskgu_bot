FROM python:3.10.9-slim

WORKDIR /rasp-bot

COPY ./requirements.txt /rasp-bot/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /rasp-bot/requirements.txt

COPY ./pskgu_bot /rasp-bot/pskgu_bot

CMD ["uvicorn", "pskgu_bot.main:app", "--host", "0.0.0.0", "--port", "80"]
