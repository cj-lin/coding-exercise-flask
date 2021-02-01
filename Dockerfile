# syntax=docker/dockerfile:experimental
# This is a simple Dockerfile to use while developing
# It's not suitable for production
#
# It allows you to run both flask and celery if you enabled it
# for flask: docker run --env-file=.flaskenv image flask run
# for celery: docker run --env-file=.flaskenv image celery worker -A myapi.celery_app:app
#
# note that celery will require a running broker and result backend
FROM python:3.7

RUN mkdir /code
WORKDIR /code

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y mariadb-client

COPY .my.cnf /root/.my.cnf
COPY requirements.txt setup.py tox.ini uwsgi.ini entrypoint.sh ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -U pip && \
    pip install -r requirements.txt && \
    pip install -e .

COPY myapi myapi/
COPY migrations migrations/
COPY tests tests/
