#!/bin/bash

exitCodeArray=()

onFailure() {
    exitCodeArray+=( "$?" )
}

trap onFailure ERR

addNumbers () {
    local IFS='+'
    printf "%s" "$(( $* ))"
}

poetry run pytest tests
poetry run pytest integration_tests

trap '' ERR

if (( $(addNumbers "${exitCodeArray[@]}") )); then
    printf 'some of your tests failed\n' >&2
    exit -1
fi
