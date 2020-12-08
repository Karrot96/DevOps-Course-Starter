#!/bin/bash

set -ev
docker build --target production --tag karrot96/todo-app:$TRAVIS_COMMIT .
docker push karrot96/todo-app:$TRAVIS_COMMIT
if [[ "$TRAVIS_BRANCH" == "master" ]]; then
    if [[ "$TRAVIS_PULL_REQUEST" == "false" ]]; then
        docker tag karrot96/todo-app:$TRAVIS_COMMIT karrot96/todo-app:latest
        docker push karrot96/todo-app:latest
    fi
fi