#!/bin/bash

cd "$(dirname "$(basename "$0")")"

docker-compose -f docker-compose.yml -f production.yml "$@"
