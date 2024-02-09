FROM python:3.12-slim

WORKDIR /

ARG test

# Upgrade pip and add google packages
RUN pip install --upgrade pip
RUN pip install keyring keyrings.google-artifactregistry-auth

# Install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /api

COPY api /api
WORKDIR /

CMD exec gunicorn --bind=:8080 --workers=4 --threads=16 --timeout=0 --log-level=INFO api.main:app
