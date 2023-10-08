FROM python:3.11.3-slim-buster

RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*


RUN pip install poetry==1.4.2

# install postgres
RUN apt-get update && apt-get install -y gcc libffi-dev python3-dev build-essential
RUN apt-get update && apt-get install -y libpq-dev gcc
# Configuring poetry
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

# Copying actual application
COPY . /app/
RUN poetry install --only main

CMD ["/usr/local/bin/python", "-m", "intree_control_panel"]
