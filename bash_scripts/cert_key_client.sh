#!/bin/bash

mkdir -p ~/client-configs/keys
chmod -R 700 ~/client-configs
cd ~/easy-rsa
./easyrsa gen-req client1 nopass

cp pki/private/client1.key ~/client-configs/keys/