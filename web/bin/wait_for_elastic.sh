#!/bin/bash
# Script that will wait for an host to be active before executing the given command.
set -e

host="$1"
shift
cmd="$@"

until curl -XGET "$host":9200; do
  >&2 echo "Elastic is still setting up..."
  sleep 1
done

echo "Elastic has completed setup, executing command."
exec $cmd