#!/bin/bash

this_path="$(dirname $BASH_SOURCE[0])"

docker compose -f "$this_path/docker-compose.yml" up \
    && docker compose -f "$this_path/docker-compose.yml" down