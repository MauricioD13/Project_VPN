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

# Certificate signature request  VPN server
./easyrsa gen-req server nopass
cp $var_home/easy-rsa/pki/private/server.key /etc/openvpn/server/

# OpenVPN cipher
openvpn --genkey --secret ta.key

cp ta.key /etc/openvpn/server



