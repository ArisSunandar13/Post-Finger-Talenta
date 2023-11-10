#! /bin/bash

echo "Deleting node_modules"
rm -rf node_modules
rm package-lock.json
rm pnpm-lock.yaml
echo

echo "Running scp command"
scp -r . aris@192.168.53.242:./post-finger-talenta
echo
echo "Done"