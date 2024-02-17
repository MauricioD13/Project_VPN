#!/bin/bash

# Variables
DOMAIN="foo.example.com"
CERTIFICATE="example.crt"
KEY_PATH="example.key"
PASSWORD=password.txt

#Create certificate in the client -> REMOVE THIS FOLLOWING LINE
step ca certificate $DOMAIN $CERTIFICATE $KEY_PATH --password-file $PASSWORD
