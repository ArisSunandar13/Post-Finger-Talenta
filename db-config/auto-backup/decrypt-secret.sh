#!/bin/bash

p1="secret1.gpg"

p2="client_secret.gpg"
p3="client_secret_desktop_app.json"

p4="token_secret.gpg"
p5="token.json"

p6=".env.gpg"
p7=".env"

# Meminta input dari pengguna
echo "Passphrase 1:"
read pass2

echo "Passphrase 2:"
read pass1

# Proses decrypt
gpg --batch --passphrase $pass1 -o $p1 -d $p2
gpg --batch --passphrase $pass2 -o $p3 -d $p1
rm $p1

gpg --batch --passphrase $pass1 -o $p1 -d $p4
gpg --batch --passphrase $pass2 -o $p5 -d $p1
rm $p1

gpg --batch --passphrase $pass1 -o $p1 -d $p6
gpg --batch --passphrase $pass2 -o $p7 -d $p1
rm $p1

echo "Done"