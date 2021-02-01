#!/usr/bin/env bash
set -e

if [[ ! -f dockerfiles/app_tests ]]; then
    echo "You have to run this script from backend root folder"
    exit 1
fi

docker-compose --file testing/docker-compose.yml up --build --exit-code-from testing --renew-anon-volumes