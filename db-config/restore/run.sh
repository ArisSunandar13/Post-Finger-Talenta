#!/bin/bash

this_path="$(dirname $BASH_SOURCE[0])"

file_name="$(ls | grep DbAbsensi-)"

mv "$this_path/$file_name" "$this_path/DbAbsensi.sql"

docker compose -f "$this_path/docker-compose.yml" up -d

mv "$this_path/DbAbsensi.sql" "$this_path/$file_name"