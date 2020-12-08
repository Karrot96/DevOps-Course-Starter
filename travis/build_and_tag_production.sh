#!/bin/bash

set -ev
docker build --target production --tag karrot96/todo-app:$TRAVIS_COMMIT .
docker push karrot96/todo-app:$TRAVIS_COMMIT
echo $TRAVIS_BRANCH
if [[ "$TRAVIS_BRANCH" == "exercise8" ]]; then
    docker push karrot96/ToDoApp:latest
fi