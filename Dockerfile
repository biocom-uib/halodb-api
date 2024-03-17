FROM python:3.12-slim

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
              build-essential \
              default-libmysqlclient-dev \
              pkg-config

# Create the mysql user manager instead of the default one, to use with a volume
RUN adduser --disabled-password --gecos "" --force-badname --gid 27  --uid 27 mysql

# Create a group and an user to avoid running the app as root
RUN addgroup --gid 1002 biocom
RUN adduser --disabled-password --gecos "" --force-badname --gid 1002 --uid 1021 halodb
RUN echo 'halodb:m3t4d4g' | chpasswd


# Upgrade pip and add google packages
RUN pip3 install --upgrade pip setuptools
RUN pip3 install keyring keyrings.google-artifactregistry-auth

# Install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir -p /opt/halodb-api
WORKDIR /opt/halodb-api

COPY api /opt/halodb-api/api
COPY static /opt/halodb-api/static
COPY sql /opt/halodb-api/sql

# Change the ownership of the /app directory to the appuser
RUN chown -R halodb:biocom /opt/halodb-api/

# Switch to the new user
# USER halodb

EXPOSE 5000

CMD exec gunicorn --bind=:5000 --workers=4 --threads=16 --timeout=0 --log-level=INFO api.main:app

