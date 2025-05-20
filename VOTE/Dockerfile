FROM ubuntu:22.04

MAINTAINER IDUG

COPY . /usr/src/vote_app
WORKDIR /usr/src/vote_app/vote_app

COPY requirements.txt ./
COPY .env ./vote_app

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-setuptools \
    python3-pip \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev

RUN pip3 install --no-cache-dir -r requirements.txt


EXPOSE 8080

CMD exec gunicorn vote_app.wsgi:application --bind 0.0.0.0:8080 --workers 3