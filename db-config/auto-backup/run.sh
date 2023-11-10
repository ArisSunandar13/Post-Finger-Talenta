#!/bin/bash

line1=$(grep "MYSQL_USER=" ".env")
line2=$(grep "MYSQL_ROOT_PASSWORD=" ".env")
line3=$(grep "MYSQL_DATABASE=" ".env")

# Memisahkan variabel dan nilai dengan menggunakan delimiter "="
IFS="=" read -ra parts1 <<< "$line1"
IFS="=" read -ra parts2 <<< "$line2"
IFS="=" read -ra parts3 <<< "$line3"

# Mengambil nilai dari variabel
user="${parts1[1]}"
password="${parts2[1]}"
database="${parts3[1]}"

docker exec mysql-absensi mysqldump -u $user -p$password $database > "$(pwd)/DbAbsensi-$(date '+%d%m%Y').sql" \
    && docker compose up \
    && docker compose down
