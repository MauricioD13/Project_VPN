#!/bin/bash

var_home=/home/ubuntu

apt update
apt -y upgrade
apt install openvpn easy-rsa

echo "-----------UPDATE SYSTEM AND INSTALL PACKAGES-------------"

# Configuration of PKI
if [ -d $var_home/easy-rsa ]; then

        echo "Directory $var_home/easy-rsa alredy exists"
else
        mkdir $var_home/easy-rsa
        ln -s /usr/share/easy-rsa/* $var_home/easy-rsa
        chown ubuntu $var_home/easy-rsa
        chmod 700 $var_home/easy-rsa
fi

cd $var_home/easy-rsa

echo 'set_var EASYRSA_ALGO "ec"
set_var EASYRSA_DIGEST "sha512"' > vars


./easyrsa init-pki

#  Certificate signature request  VPN server
./easyrsa gen-req server nopass


echo "-------------COPY THIS REQUEST TO CA SERVER------------"
cat $var_home/easy-rsa/pki/reqs/server.req

echo "------------INTRODUCE COPY SERVER.CRT FILE-----------"
read server_crt

echo $server_crt > /etc/openvpn/server/server.crt

echo "-------------INTRODUCE COPY CA:CRT FILE--------------"
read ca_crt

echo $ca_crt > /etc/openvpn/server/ca.crt
