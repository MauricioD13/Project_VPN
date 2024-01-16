import boto3
from botocore.exceptions import ClientError
import paramiko
import time

ec2 = boto3.client('ec2')

# Create key pair
key_pair = ec2.create_key_pair(KeyName='myKey')
private_key = key_pair['KeyMaterial']

# Save private key to file
with open('my_key.pem', 'w') as key_file:
    key_file.write(private_key) 

# Set user data script
user_data = """
#!/bin/bash
yum update -y
yum install -y httpd
service httpd start
chkconfig httpd on
echo "<h1>Hello World</h1>" > /var/www/html/index.html
"""

# Launch EC2 instance
instances = ec2.run_instances(
    ImageId='ami-0aab3940ccac14a65', # Amazon Linux 2 AMI
    InstanceType='t2.micro',
    KeyName='myKey',
    UserData=user_data,
    MaxCount=1,
    MinCount=1
)

instance_id = instances['Instances'][0]['InstanceId']

# Wait for instance to run
waiter = ec2.get_waiter('instance_status_ok') 
waiter.wait(InstanceIds=[instance_id])

# Get public DNS name
instance = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
public_dns = instance['PublicDnsName']

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