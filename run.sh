#!/bin/bash

poetry run gunicorn -w 2 --threads 2 --bind 0.0.0.0:8003 'todo_app.app:create_app()'

exec $@