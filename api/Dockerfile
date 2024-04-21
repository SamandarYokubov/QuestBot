FROM python:3.12

WORKDIR /code

COPY ./api/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY ./api .

ENTRYPOINT uvicorn app.main:app --host 0.0.0.0 --port 80