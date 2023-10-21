#!/bin/bash
#

#scp -i access_file.pem -P port remote_host:file_to_retrive destination_directory


var_home=$1

cd $var_home/easy-rsa

./easyrsa import-req server.req server

./easyrsa sign-req server server


echo "----PUBLIC KEY SERVER CRT----------"
cat pki/issued/server.crt

echo "--------CA CRT-------------"
cat pki/ca.crt
