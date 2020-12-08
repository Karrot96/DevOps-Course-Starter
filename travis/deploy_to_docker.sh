#!/bin/bash sh

set -ev
if [[ "$TRAVIS_BRANCH" == "master" ]]; then
    docker pull karrot96/todo-app:latest
    docker tag karrot96/todo-app:latest registry.heroku.com/karro96-todo-app/web
    docker push registry.heroku.com/karro96-todo-app/web
fi