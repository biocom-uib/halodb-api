FROM python:3.12-slim as base

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
              build-essential \
              default-libmysqlclient-dev \
              pkg-config

# Upgrade pip and add google packages
RUN pip3 install --upgrade pip setuptools
RUN pip3 install keyring keyrings.google-artifactregistry-auth

# Install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir -p /opt/halodb-api
WORKDIR /opt/halodb-api

# Create a group and an user to avoid running the app as root
RUN addgroup --gid 1002 biocom
RUN adduser --disabled-password --gecos "" --force-badname --gid 1002 --uid 1021 halodb

COPY --chown=halodb:biocom static /opt/halodb-api/static
COPY --chown=halodb:biocom sql /opt/halodb-api/sql

# Switch to the new user
USER halodb

EXPOSE 5000

CMD exec gunicorn --reload --bind=:5000 --workers=1 --threads=2 --timeout=0 --log-level=DEBUG api.main:app


FROM base as production

COPY --chown=halodb:biocom api /opt/halodb-api/api

CMD exec gunicorn --bind=:5000 --workers=4 --threads=16 --timeout=0 --log-level=INFO --log-file=/var/log/halodb-api/app.log api.main:app
