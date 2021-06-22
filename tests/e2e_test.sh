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

poetry run pytest e2e_tests

trap '' ERR

if (( $(addNumbers "${exitCodeArray[@]}") )); then
    printf 'e2e tests failed\n' >&2
    exit -1
fi
