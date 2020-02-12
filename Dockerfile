FROM python:3.7.5-alpine3.10

ARG HOST
ARG PORT

ENV HOST $HOST
ENV PORT $PORT
ENV PIP app
ENV PYTHON python

WORKDIR /app

ADD . /app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev && \
     pip install -r requirements.txt --no-cache-dir --upgrade pip

ENTRYPOINT sh ./entrypoint.sh
