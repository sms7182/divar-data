FROM python:3.8-slim-buster

WORKDIR /app

COPY torob.py torob.py
COPY fetch-data.py fetch-data.py


RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

CMD [ "python3","./torob.py" ]

