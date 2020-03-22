#!/bin/sh
python3 codehub/manage.py migrate --noinput
python3 codehub/manage.py collectstatic --noinput

cd codehub
daphne -b 0.0.0.0 -p 8000 codehub.asgi:application
