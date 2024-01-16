import subprocess
"""
This file have to be executed in a linux enviroment and in the local machine that would be the CA server for signing the request certificates

result = subprocess.run(["dir"], shell=True, capture_output=True, text=True)

print(result.stdout)"""

def copy_to_local(remote_file, dst_dir):
    """Function to copy any file to a destination directory in the local machine

    Args:
        remote_file (str): remote file to copy to local
        dst_dir (str): local directory file
    """
    result = subprocess.run([f"scp -i ~/EC2_VPN.pem ec2-user@ec2-54-234-65-11.compute-1.amazonaws.com:~/home/ubuntu/{remote_file} ~/Project_VPN/{dst_dir}"])    
    print(f"Result SCP: {result.stdout.decode()}")

def CA_server():
    """Create a CA server in the PC
    """
    result = subprocess.run(["./bash_scripts/CA_server.sh"], shell=True, capture_output=True, text=True)
    print(result.stdout.decode())
    
def server_VPN():
    """Execute the server_VPN.sh file which install packages, create directories and files, and Init PKI
    """
    result = subprocess.run(["./bash_scripts/erver_VPN.sh"], shell=True, capture_output=True, text=True)                       
    print(result.stdout.decode())
    
def sign_req_server():
    test = subprocess.run(["pwd"],shell=True, capture_output=True, text=True)
    var_home = test.stdout.decode()
    result = subprocess.run([f"./bash_scripts/sign_req.sh {var_home} server"], shell=True, capture_output=True, text=True)
    copy_to_local("pki/issued/server.crt","certificates")
    copy_to_local("pki/ca.crt","certificates")
    print(result.stdout.decode())

def recover_request():
    #result = subprocess.run(["scp -i ~/EC2_VPN.pem ec2-user@ec2-54-234-65-11.compute-1.amazonaws.com:~/home/ubuntu/easy-rsa/pki/reqs/server.req ~/Project_VPN/requests"], shell=True, capture_output=True, text=True)
    copy_to_local("easy-rsa/pki/reqs/server.req")
    print(result.stdout.decode())

def sign_req_client():
    result = subprocess.run([f"./cert_key_client.sh"])
    copy_to_local("pki/reqs/client1.req","requests")
    

def main():
    
    CA_server()
    server_VPN()
    recover_request()
    sign_req_server()
    sign_req_client()
    
    
# Certificate signature request  VPN server

