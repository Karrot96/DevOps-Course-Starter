#!/bin/bash

set -ev
docker build --target production --tag karrot96/ToDoApp:$TRAVIS_COMMIT .
docker push karrot96/ToDoApp:$TRAVIS_COMMIT
if [[ "$TRAVIS_BRANCH" == "master" ]]; then
    docker push karrot96/ToDoApp:latest
fi