import boto3
from botocore.exceptions import ClientError
import paramiko
import time
import subprocess
import os
from network_objects import security_group_create, create_vpc
"""
result = subprocess.run(["dir"], shell=True, capture_output=True, text=True)

print(result.stdout)"""


def create_key_pair(key_name):
    try:
        key_pair = ec2.create_key_pair(KeyName=key_name)
        private_key = key_pair["KeyMaterial"]
    except ClientError as e:
        print(
            "Key pair already exists, proceeding to eliminate it and create a new one"
        )
        response = ec2.delete_key_pair(KeyName=key_name)
        key_pair = ec2.create_key_pair(KeyName=key_name)
        private_key = key_pair["KeyMaterial"]
    return private_key



# Create boto client for EC2 Instance
ec2 = boto3.client("ec2", region_name="us-east-2")

# Create key pair
if os.path.exists("keys/") and not ec2.describe_key_pairs()["KeyPairs"]:
    if not os.path.exists("vpn_key.pem"):
        private_key = create_key_pair("vpn_key")
else:
    # Create directory for keys
    subprocess.run(["mkdir", "keys"], capture_output=True, text=True)
    subprocess.run(["touch", "/keys/vpn_key.pem"], capture_output=True, text=True)
    private_key = create_key_pair("vpn_key")

# Save private key to file
with open("keys/vpn_key.pem", "w") as key_file:
    key_file.write(private_key)

# Set user data script
with open("bash_scripts/server_VPN.sh") as file:
    user_data = file.read()

# Create security group
security_group_id = security_group_create(ec2)
print("Security group ID outside: ", security_group_id)

# Launch EC2 instance
instances = ec2.run_instances(
    ImageId="ami-05fb0b8c1424f266b",  # Ubuntu Linux 22.04
    InstanceType="t2.micro",
    KeyName="vpn_key",
    UserData=user_data,
    MaxCount=1,
    MinCount=1,
    SecurityGroups=[security_group_id],
)

instance_id = instances["Instances"][0]["InstanceId"]

# Wait for instance to run
print("Waiting for instance to run...")
waiter = ec2.get_waiter("instance_status_ok")
waiter.wait(InstanceIds=[instance_id])

# Get public DNS name
instance = ec2.describe_instances(InstanceIds=[instance_id])["Reservations"][0][
    "Instances"
][0]
print(f"Instance: {instance} is running")
public_dns = instance["PublicDnsName"]

# Connect via SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

while True:
    try:
        print(f"Connecting to {public_dns}")
        ssh.connect(hostname=public_dns, username="ec2-user", key_filename="my_key.pem")
        print("Connected!")
        break
    except:
        print("Connection failed, retrying...")
        time.sleep(10)

# Interact with EC2 instance
stdin, stdout, stderr = ssh.exec_command("uname -a")
print(stdout.read().decode())

ssh.close()
