#!/bin/sh
docker compose -f ./infrastructure/docker-compose.yml build
docker compose -f ./infrastructure/docker-compose.yml up