FROM python:3.8.0-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev redis

RUN redis-server
RUN redis-cli ping
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/



RUN pip install -r requirements.txt
COPY . /code/

RUN python manage.py makemigrations
RUN python manage.py migrate
# create admin and normal user
# loading teams to db
RUN python manage.py loaddata teams