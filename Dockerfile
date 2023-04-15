FROM python:3.11.3-slim-buster

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y libpq-dev gcc

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/