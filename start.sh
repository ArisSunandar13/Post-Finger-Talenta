#!/bin/bash

this_path="$(dirname $BASH_SOURCE[0])"

if [ ! -d "$this_path/node_modules" ]; then
    npm --prefix $this_path install $this_path
fi \
    && node post_fingerprint.js
