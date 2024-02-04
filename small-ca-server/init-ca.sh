#!/bin/sh

# Generate root certificate
step certificate create root_ca.crt root_ca.key 

# Initialize CA
step ca init --address 0.0.0.0:8080 --dns localhost --provisioner admin@smallstep.com --password pass --root root_ca.crt --root-key root_ca.key

# Run CA server
step-ca $ARGS