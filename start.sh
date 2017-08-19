#!/bin/bash

./manage.py collectstatic --noinput
./manage.py migrate
exec gunicorn wifidb.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
