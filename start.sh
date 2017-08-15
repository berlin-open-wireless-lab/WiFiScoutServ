#!/bin/bash

./manage.py collectstatic --noinput
./manage.py migrate
exec gunicorn wifidb.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-logfile access.log \
    --error-logfile error.log \
    --log-level debug
