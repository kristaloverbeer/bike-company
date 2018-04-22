FROM python:3.6-alpine

WORKDIR /src
COPY . /src

ENV PYTHONPATH /src

RUN apk update \
    && apk add --virtual build-deps gcc python-dev musl-dev \
    && pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080
