FROM python:3.12-slim

WORKDIR /

ARG test


ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
	      unzip \
              openssh-server \
              vim \
              supervisor

# Upgrade pip and add google packages
RUN pip install --upgrade pip
RUN pip install keyring keyrings.google-artifactregistry-auth

# Install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN addgroup --gid 1002 biocom
RUN adduser --disabled-password --gecos "" --force-badname --gid 1002 --uid 1004 metadag
#RUN echo 'm3t4d4g\nm3t4d4g' | passwd metadag
RUN echo 'metadag:m3t4d4g' | chpasswd


WORKDIR /api

COPY api /api
COPY static /static
COPY sql /sql
WORKDIR /

EXPOSE 22 5000

CMD exec gunicorn --bind=:5000 --workers=4 --threads=16 --timeout=0 --log-level=INFO --log-file=/var/log/haldodb.log api.main:app
