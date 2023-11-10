#!/bin/bash

p1="secret1.gpg"

p2="client_secret.gpg"
p3="client_secret_desktop_app.json"

p4="token_secret.gpg"
p5="token.json"

p6=".env.gpg"
p7=".env"

# Meminta input dari pengguna (base64) echo <string> | base64
echo "Passphrase 1:"
read pass1

echo "Passphrase 2:"
read pass2

# Proses encrypt
rm $p2
gpg --batch --passphrase $pass1 -o $p1 -c $p3
gpg --batch --passphrase $pass2 -o $p2 -c $p1
rm $p1

rm $p4
gpg --batch --passphrase $pass1 -o $p1 -c $p5
gpg --batch --passphrase $pass2 -o $p4 -c $p1
rm $p1

rm $p6
gpg --batch --passphrase $pass1 -o $p1 -c $p7
gpg --batch --passphrase $pass2 -o $p6 -c $p1
rm $p1

echo "Done"