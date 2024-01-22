FROM python:3.11.3-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
  apt-get install -y libpq-dev python3-dev python-dev python-psycopg2 python3-psycopg2 gcc

RUN pip install poetry==1.4.2

RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/
WORKDIR /app

# Installing requirements
RUN poetry install --only main

# Removing gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
