FROM python:3.12

WORKDIR /code

COPY ./quest_gen_service/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY ./quest_gen_service .

ENTRYPOINT python server.py