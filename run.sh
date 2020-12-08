#!/bin/bash

if [ "$1" = "prod" ]; then
    poetry run gunicorn -w 2 --threads 2 --bind 0.0.0.0:$PORT 'todo_app.app:create_app()'
fi

if [ "$1" = "dev" ]; then
    cd todo_app
    poetry run flask run --host=0.0.0.0
fi

exec $@