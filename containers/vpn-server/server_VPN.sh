#!/bin/bash


apk update
apt -y upgrade
apt install openvpn easy-rsa


# OpenVPN cipher
openvpn --genkey --secret ta.key

cp ta.key /etc/openvpn/server

CA_FINGERPRINT=$(docker run -v step:/home/step smallstep/step-ca step certificate fingerprint certs/root_ca.crt) step ca bootstrap --ca-url https://localhost:9000 --fingerprint $CA_FINGERPRINT



