#!/bin/bash

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