#!/bin/bash
set -exo pipefail
docker-compose down --volumes --remove-orphans

docker build  --target development . -t todo_app:dev
docker-compose -f docker-compose.yml up -d

