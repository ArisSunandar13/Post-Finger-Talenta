#! /bin/bash

echo "Deleting node_modules"
rm -rf node_modules
rm package-lock.json
rm pnpm-lock.yaml
rm *.log
rm ./db-config/auto-backup/*.log
echo

sending_list="db-config \
    .dockerignore \
    .env \
    .env.gpg \
    .gitignore \
    db_to_csv.py \
    docker-compose.yml \
    Dockerfile \
    package.json \
    post_fingerprint.js \
    run.sh \
    scp.sh \
    update_status.py"

echo "Running scp command"
scp -r $sending_list aris@192.168.53.242:./post-finger-talenta
echo
echo "Done"