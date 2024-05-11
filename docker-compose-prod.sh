#!/bin/bash

cd "$(basename "$0")"

docker-compose -f docker-compose.yml -f production.yml "$@"
