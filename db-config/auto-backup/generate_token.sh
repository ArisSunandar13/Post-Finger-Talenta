#!/bin/bash

docker run --rm -it --volume .:/app auto-backup-post-to-drive sh -c "python3 generate_token.py"
