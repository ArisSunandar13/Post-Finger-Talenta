#!/bin/bash

docker build -t auto-backup-post-to-drive . \
    &&  docker run --rm -it --volume .:/app auto-backup-post-to-drive sh -c "python3 generate_token.py"
