import subprocess
"""
result = subprocess.run(["dir"], shell=True, capture_output=True, text=True)

print(result.stdout)"""
# Create CA server 

def CA_server():
    result = subprocess.run(["./CA_server.sh"], shell=True, capture_output=True, text=True)
    print(result)
    
def server_VPN():
    result = subprocess.run(["./server_VPN.sh"], shell=True, capture_output=True, text=True)                       
    print(result)
    
def sign_req():
    result = subprocess.run(["./sign_req.sh"], shell=True, capture_output=True, text=True)
    print(result)
    
def main():
    
    CA_server()
    server_VPN()
    
# Certificate signature request  VPN server

