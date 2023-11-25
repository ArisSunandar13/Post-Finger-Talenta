#!/bin/bash

docker run --rm -it --volume .:/app auto-backup-post-to-drive sh

# RUN :
# 1. typing: "python3 upload_to_drive.py" on terminal
# 2. open link URL
# 3. login with IT TMS
# 4. check all
# 5. copy authorization code
# 6. enter the authorization code
# 7. typing: "exit" on terminal
# Done