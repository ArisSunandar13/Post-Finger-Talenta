#!/bin/bash

this_path="$(dirname $BASH_SOURCE[0])"

filename="$(ls | grep DbAbsensi)"

new_filename="DbAbsensi.sql"

mv "$this_path/$filename" "$this_path/$new_filename" \
    && docker compose -f "$this_path/docker-compose.yml" up -d \
    && mv "$this_path/$new_filename" "$this_path/$filename"
