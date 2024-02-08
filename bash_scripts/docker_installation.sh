#!/bin/bash

apt update

apt install -y docker.io

systemctl start docker

systemctl enable docker

usermod -a -G docker ubuntu

