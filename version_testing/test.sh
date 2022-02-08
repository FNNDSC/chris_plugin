#!/bin/bash -e

if [ -z "$1" ]; then
  >&2 echo "usage: $0 IMAGE"
  exit 1
fi

python_version=$(docker inspect -f '{{ index .Config.Labels "org.chrisproject.python_version" }}' $1)
>&2 printf "Running tests for version %s: " "$python_version"

exec docker run --rm -t \
  -v $(realpath ..)/chris_plugin:/usr/local/src/chris_plugin/chris_plugin $1
