FROM python:3.12

WORKDIR /code

COPY ./bot/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY ./bot .

ENTRYPOINT python bot.py
