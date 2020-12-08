#!/bin/bash

set -ev
if [[ "$TRAVIS_BRANCH" == "master" ]]; then
    if [[ "$TRAVIS_PULL_REQUEST" == "true" ]]; then
        docker pull karrot96/todo-app:latest
        docker tag karrot96/todo-app:latest registry.heroku.com/karro96-todo-app/web
        docker push registry.heroku.com/karro96-todo-app/web
        docker login --username=alex.karet@softwire.com --password=$HEROKU_TOKEN registry.heroku.com
        heroku container:release web
    fi
fi