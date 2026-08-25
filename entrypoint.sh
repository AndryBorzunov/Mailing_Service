#!/bin/sh
if [ "$ENVIRONMENT" = "production" ]; then
    exec poetry run gunicorn -c gunicorn.conf.py
else
    exec poetry run python manage.py runserver 0.0.0.0:8000
fi
