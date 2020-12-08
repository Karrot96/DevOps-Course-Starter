#!/bin/bash

set -ev
if [[ "$TRAVIS_BRANCH" == "master" ]]; then
    if [[ "$TRAVIS_PULL_REQUEST" != "false" ]]; then
        docker pull karrot96/todo-app:latest
        docker tag karrot96/todo-app:latest registry.heroku.com/karro96-todo-app/web
        docker push registry.heroku.com/karro96-todo-app/web
        heroku container:login
        heroku container:release web --app karro96-todo-app
    fi
fi