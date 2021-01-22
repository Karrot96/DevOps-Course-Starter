#!/bin/bash

set -ev
docker build --target production --tag karrot96/todo-app:$TRAVIS_COMMIT --cache-from karrot96/todo-app .
docker push karrot96/todo-app:$TRAVIS_COMMIT
docker tag karrot96/todo-app:$TRAVIS_COMMIT karrot96/todo-app:latest
docker push karrot96/todo-app:latest