# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev netcat-openbsd build-base

RUN apk add --no-cache \
        libressl-dev \
        musl-dev \
        libffi-dev && \
    pip install --no-cache-dir cryptography==3.2.1 && \
    apk del \
        libressl-dev \
        musl-dev \
        libffi-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt



# copy project
COPY . .