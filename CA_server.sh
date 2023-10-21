#!/bin/bash
echo "--------UPDATING SYSTEM-------------"

var_home=/home/guasonito

apt update
apt upgrade -y

echo "--------UPDATING SYSTEM DONE----------"

echo "--------INSTALLING PACKAGE------------"

apt install easy-rsa


echo "---------MAKING DIR AND INIT PKI------------"
if [ -d $var_home/easy-rsa ]; then
	echo "Directory $var_home/easy-rsa already exists"
else
	mkdir $var_home/easy-rsa
	ln -s /usr/share/easy-rsa/* $var_home/easy-rsa/
	chown guasonito $var_home/easy-rsa
	chmod 700 $var_home/easy-rsa
fi

cd $var_home/easy-rsa

./easyrsa init-pki


touch vars

echo 'set_var EASYRSA_REQ_COUNTRY    "CO"
set_var EASYRSA_REQ_PROVINCE   "Bogota"
set_var EASYRSA_REQ_CITY       "Bogota City"
set_var EASYRSA_REQ_ORG        "My Organization"
set_var EASYRSA_REQ_EMAIL      "admin@example.com"
set_var EASYRSA_REQ_OU         "Community"
set_var EASYRSA_ALGO           "ec"
set_var EASYRSA_DIGEST         "sha512"
' >> vars

./easyrsa build-ca nopass

echo "----------------CA SERVER COMPLETE------------"
