terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-2"
}

resource "aws_instance" "app_server" {
  ami                         = "ami-05bdb477706e2a189"
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.vpn_subnet.id
  associate_public_ip_address = true
  security_groups             = aws_security_group.ssh.id
  key_name                    = "server_docker"
  tags = {
    Name = "server-docker"
  }
}

resource "aws_vpc" "vpn_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "tf_vpn_vpc"
  }
}

resource "aws_subnet" "vpn_subnet" {

  vpc_id     = aws_vpc.vpn_vpc.id
  cidr_block = "10.0.1.0/24"
  tags = {
    Name = "tf_vpn_subnet"
  }
}

resource "aws_security_group" "ssh" {
  name        = "ssh-sg"
  description = "Allow ssh access"
  vpc_id      = aws_vpc.vpn_vpc.id

  ingress {
    description = "SSH from everywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ssh-sg"
  }
}