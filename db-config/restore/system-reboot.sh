#!/bin/bash

this_path="$(dirname $BASH_SOURCE[0])"

docker compose -f "$this_path/docker-compose.yml" down \
    && docker compose -f "$this_path/docker-compose.yml" up -d

rm -r "$this_path/DbAbsensi.sql"