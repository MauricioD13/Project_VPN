#!/bin/bash
#

#scp -i access_file.pem -P port remote_host:file_to_retrive destination_directory


var_home=$1
type_sign=$2

cd $var_home/easy-rsa

if [ $type_sign == "server"]; then
    ./easyrsa import-req server.req $type_sign
else
    echo "client"

./easyrsa sign-req server server


#pki/issued/server.crt
#pki/ca.crt
